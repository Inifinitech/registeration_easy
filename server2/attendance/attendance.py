from flask import Blueprint, make_response, request
from models import Attendance, db
from flask_restful import Api, Resource

attendances = Blueprint("attendances", __name__)
api=Api(attendances)

# creating an Attendances Resource 
class Attendences(Resource):
    # creating a get method to get all attendances
    def get(self):
        # Querying the database to get all the attendances
        attendances = Attendance.query.all()
        # Looping through the attendances to get one attendance in form of a dictionary
        attendance_dict = [attendance.to_dict() for attendance  in attendances]
        # creating and returning a response
        response = make_response(attendance_dict, 200)
        return response
    
    # creating a method to post new attendances
    def post(self):
        # creating new attendance
        data = request.get_json()
        new_attendance = Attendance(
            date = data["date"],
            status = data["status"],
            member_id = data["member_id"]
        )

        if new_attendance:
            # adding and commiting the attendance to the database
            db.session.add(new_attendance)
            db.session.commit()
            # making the new_attendance to a dictionary
            new_attendance_dict = new_attendance.to_dict(rules=("-member.ag_group", ))
            # creating and returning a response
            response = make_response(new_attendance_dict, 201)
            return response
        else:
            # creating and returning a response based on the response body
            response_body = {"message": "some field is missing"}
            response = make_response(response_body, 400)
            return response
    pass

# creating AttendanceById Resource
class AttendanceById(Resource):
    # a get method to get one attendance with a specific id 
    def get(self, id):
        # querying the database using the id 
        attendance1 = Attendance.query.filter_by(id=id).all()
        if attendance1:
            # making the attendance to a dictionary
            attendance_dict = [attendance.to_dict(rules = ("-member.ag_group",)) for attendance in attendance1]
            # creating and returning a response 
            response = make_response(attendance_dict, 200)
            return response
        else:
            # creating and returning a response based on the response_body
            response_body = {"message":f"The attendance with id of {id}  is not found"}
            response = make_response(response_body, 400)
            return response
    
    #  a patch method to update attendance details
    def patch(self, id):
        # querying the database and filtering it using the id 
        attendance = Attendance.query.filter_by(id=id).first()

        if attendance:
            # getting the data from the requests made 
            data = request.get_json()

            # using setattr to set the attr and data
            for attr in data:
                setattr(attendance, attr, data[attr])
            
            # commiting the changes to the database
            db.session.commit()

            # converting the attendance to a dictionary using to_dict method
            attendance_dict = attendance.to_dict()
            # creating and returning a response 
            response = make_response(attendance_dict, 200)
            return response
        else:
            # creating and returning a response based on the response body
            response_body = {"message": f"The attendance with the id of {id} is not found"}
            response = make_response(response_body, 400)
            return response
    
    # a method to delete an attendance based on the Id
    def delete(self, id):
        # querying and filtering the database using the id 
        attendance = Attendance.query.filter_by(id = id).first()

        if attendance:
            # Deleting the attendance from the database
            db.session.delete(attendance)
            db.session.commit()

            # creating and returning a response based on the response_body
            response_body = {"message":f"The attendance with the id of {id} has been deleted successfully"}
            response = make_response(response_body, 204)
            return response
        else:
            # creating and returning a response based on the response body
            response_body = {"message":f"The attendance with the id of {id} is not found"}
            response = make_response(response_body, 400)
            return response
    pass

api.add_resource(Attendences, "/attendances", endpoint="attendances")
api.add_resource(AttendanceById, "/attendances/<int:id>", endpoint="attendance_by_id")