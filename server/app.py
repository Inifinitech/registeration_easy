from flask import Flask,make_response,request,jsonify,session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from sqlalchemy import func, desc
from flask_cors import CORS

from models import db,Group,Attendance,Member,MemberEvent,Event,Admin, EmergencyContact
from flask_restful import Resource,Api
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import os
import logging

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] ="sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True 

migrate=Migrate(app,db)
db.init_app(app)
api=Api(app)
bcrypt=Bcrypt(app)
CORS(app)

#secret key
app.secret_key=os.urandom(24)

#Endpoints
@app.before_request
def before_login():
    protected_endpoints=['admins']
    if request.endpoint in protected_endpoints and request.method =='GET' and 'user_id' not in session:
        return jsonify (
            {
                "message":"Please log in"
            }
            
        )

class AdminRegistry(Resource):
    def post(self):
        data = request.get_json()

        dob_str = data['dob']
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

        # Create a new member instance
        new_member = Member(
            first_name=data['first_name'],
            last_name=data['last_name'],
            gender_enum=data['gender_enum'],
            dob=dob,
            location=data['location'],
            phone=data['phone'],
            is_student=data['is_student'],
            will_be_coming=data['will_be_coming'],
            is_visitor=data['is_visitor'],
            school=data.get('school'),
            occupation=data['occupation'],
            group_id=data['group_id'],
            created_at=datetime.now()
        )

        try:
            db.session.add(new_member)
            db.session.commit()  # Commit to generate the new_member.id
        except Exception as e:
            db.session.rollback()
            return {'error': f"Failed to save member: {str(e)}"}, 500

        # Add emergency contacts with the new member's ID
        emergency_contacts = data.get("emergency_contact_id", [])
        for emergency_contact in emergency_contacts:
            emergency_contact_data = EmergencyContact(
                name=emergency_contact.get('name'),
                phone=emergency_contact.get('phone'),
                relation=emergency_contact.get('relation'),
                member_id=new_member.id  # Use the ID of the newly created member
            )
            db.session.add(emergency_contact_data)

        # Commit the emergency contacts
        try:
            db.session.commit()
            return make_response(new_member.to_dict(rules=('-group.members', )), 201)
        except Exception as e:
            db.session.rollback()
            return {'error': f"Failed to save emergency contacts: {str(e)}"}, 500


            
    def get(self):
        # members = [member.to_dict(rules=('-group.members','-attendances', '-events','-memberevents',)) for member in Member.query.all()]
        # return members, 200
        members_dict = []
        
        # Fetch the latest 5 members based on created_at
        latest_members = Member.query.order_by(Member.created_at.desc()).limit(5).all()
        
        for member in latest_members:
            member_info = member.to_dict(only=('first_name', 'last_name', 'gender_enum', 'dob', 'location',
                                               'phone', 'is_student', 'will_be_coming', 'is_visitor', 'school', 'occupation'))

            # Add group name
            group_name = member.group.name if member.group else "No Group"

            # Add emergency contacts
            emergency_contact_info = []
            for contact in member.emergency_contacts:
                emergency_contact_info.append({
                    'name': contact.name,
                    'phone': contact.phone,
                    'relation': contact.relation
                })

            # Update member_info with additional data
            member_info.update({
                'group_name': group_name,
                "emergency_contacts": emergency_contact_info
            })

            members_dict.append(member_info)
        
        return make_response(members_dict, 200)

    
class HomeMembers(Resource):

     def get(self):
        # if 'user_id' not in session:
        #     return {"message":"Please Login in to acess resources"}
        members_dict = []
        for member in Member.query.all():
            member_info = member.to_dict(only=('first_name', 'last_name','gender_enum','dob','location'
                                               ,'phone','is_student','will_be_coming','is_visitor','school','occupation'))

            group_name = member.group.name 
            # 'emergency_contact_name': member.emergency_contacts.name,
            # 'emergency_contact_phone': member.emergency_contacts.phone 

            emergency_contact_info = []
            for contact in member.emergency_contacts:
                emergency_contact_info.append({
                    'name': contact.name,
                    'phone': contact.phone,
                    'relation': contact.relation
                })

            member_info.update({
                'group_name': group_name,
                "emergency_contacts": emergency_contact_info
            })   
            

            members_dict.append(member_info)
        return make_response(members_dict, 200)
         
class HomeMember_name(Resource):
    def get(self, name):
        members = Member.query.filter(Member.first_name == name).first()
        if members:
            member_dict = members.to_dict(only=('first_name', 'last_name')) |  {'group_name': members.group.name}
            response = make_response(member_dict, 200)
            return response
        else:
            response_body = {
                "error": "member not found"
            }
            return make_response(response_body, 404)
        
    
class AdminMemberSearch(Resource):
    def get(self, id):
        member = Member.query.filter(Member.first_name==id).first()
        if member:
            member_dict = member.to_dict(rules=('-group.members','-attendances', '-events','-memberevents',))
            response = make_response(member_dict, 200)
            return response
        else:
            response_body = {
                "error": "member not found"
            }
            return make_response(response_body, 404)
        
    def patch(self, id):
        member = Member.query.filter(Member.id==id).first()
        if member:
            # loop to get the attributes
            data = request.get_json()
            for attr in data:
                setattr(member, attr, data[attr])

            db.session.commit()
            return make_response(jsonify(member.to_dict(rules=('-group.members','-attendances', '-events','-memberevents',))), 200)
        else:
            response_body = {"error": "Member not found"}
            response = make_response(response_body, 400)
            return response

class MemberDelete(Resource):
    def delete(self, id):
        member = Member.query.filter(Member.id==id).first()
        
        if not member:
            return {"error": f"Member {id} not found"}, 400
        
        db.session.delete(member)
        db.session.commit()

        response_dict = {"message": f"Member {id} deleted successfully"}
        response = make_response(response_dict, 200)
        return response
        
class AttendanceDetails(Resource):
    def get(self):
        try:
            total_members = Member.query.all()
            attendance_data = []

            for member in total_members:
                attendance = Attendance.query.filter_by(member_id=member.id).first()
                
                if attendance is not None:
                    attendance_info = {
                        'id': member.id,
                        'first_name': member.first_name,
                        'last_name': member.last_name,
                        'date': attendance.date, 
                        'present': attendance.status == 'present'
                    }
                else: 
                    attendance_info = {
                        'id': member.id,
                        'first_name': member.first_name,
                        'last_name': member.last_name,
                        'date': 'N/A',
                        'present': False
                    }
                
                attendance_data.append(attendance_info)

            # Return a properly formatted JSON response
            return jsonify(attendance_data)

        except Exception as e:
            response = {'error': str(e)}
            return make_response(jsonify(response), 500)



class AttendanceReports(Resource):
    def get(self):
        # Expecting a date to be passed as a query parameter
        selected_date = request.args.get('date')

        if not selected_date:
            return make_response(jsonify({'error': 'Date parameter is required'}), 400)

        try:
            # Fetch all members
            total_members = Member.query.all()
            attendance_data = []

            for member in total_members:
                # Fetch attendance record for the specific date
                attendance = Attendance.query.filter_by(member_id=member.id, date=selected_date).first()
                
                if attendance:
                    attendance_info = {
                        'id': member.id,
                        'first_name': member.first_name,
                        'last_name': member.last_name,
                        'date': attendance.date.strftime('%Y-%m-%d'),  # Format the date as needed
                        'present': attendance.status == 'present'
                    }
                else: 
                    attendance_info = {
                        'id': member.id,
                        'first_name': member.first_name,
                        'last_name': member.last_name,
                        'date': selected_date,  # Still show the date
                        'present': False
                    }
                
                attendance_data.append(attendance_info)

            # Return a properly formatted JSON response
            return jsonify(attendance_data)

        except Exception as e:
            response = {'error': str(e)}
            return make_response(jsonify(response), 500)
        
class Admins(Resource):

    def get(self):
        admins_dict = [admin.to_dict(only=('id', 'username')) for admin in Admin.query.all()]
        return make_response(admins_dict, 200)
    
    def post(self):
        username=request.json["username"]
        password=request.json["password"]

        hashed_pass=bcrypt.generate_password_hash(password).decode("utf-8")
        new_user=Admin(username=username,password=hashed_pass)
        db.session.add(new_user)
        db.session.commit()
        return {
            "message":"User succesfully created"
        }
    

class Login(Resource):
    def post(self):
        username = request.json.get("username")
        password = request.json.get("password")  

        user=Admin.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password,password):
            session["user_id"]=user.id

            return make_response( {
            "message":"Login successfull"
         },200)
        return make_response({
            "message":"Invalid Credentials"
        },401)
    
class Logout(Resource):
    def post(self):
        session.pop('user_id',None)

        return jsonify({
            "message":"Logout sucessfully"
        })


api.add_resource(HomeMembers, '/members')
api.add_resource(HomeMember_name, '/homemembers/<string:name>')
api.add_resource(AdminRegistry, '/adminregistry')
api.add_resource(AdminMemberSearch, '/adminsearch/<int:id>')
api.add_resource(MemberDelete, '/delete/<int:id>')
api.add_resource(AttendanceReports, '/reports')
api.add_resource(AttendanceDetails, '/attendancedetails')
api.add_resource(Admins,'/admins')
api.add_resource(Login,'/login')
api.add_resource(Logout,'/logout')



if __name__ == '__main__':
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host="0.0.0.0", port=port, debug=True)
    app.run(port=5000, debug=True)