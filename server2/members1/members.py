from models import Member, Contact, db
from flask import Blueprint, make_response, request
from flask_restful import Api, Resource
from datetime import datetime

members = Blueprint("members", __name__)
api = Api(members)

# creating a Home resource
class Home(Resource):
    def get(self):
        #  creating and returning a response based on the response body
        response_body = {"Message": "Welcome to Registration Easy"}
        response = make_response(response_body, 200)
        return response
    pass

# creating a Members Resource
class Members(Resource):
    # creating a get method that gets all members
    def get(self):
        # Querying the database to get all the members
        members = Member.query.all()
        # Looping through all members to get one member in a dictionary form of display
        member1 = [member.to_dict() for member in members]
        # creating and returning a response 
        response = make_response(member1, 200)
        return response
    
    #  creating a method to post new members
    def post(self):
        #  creating a new member out of the users input
        data =request.get_json()

        # Convert the date_of_birth string into a datetime object
        try:
            # Assuming the format is "DD/MM/YYYY"
            date_of_birth = datetime.strptime(data["date_of_birth"], "%d/%m/%Y")
        except ValueError:
            response_body = {"message": "Invalid date format. Use DD/MM/YYYY."}
            response = make_response(response_body, 400)
            return response
        
        new_member = Member(
            first_name = data["first_name"],
            last_name = data["last_name"],
            surname = data["surname"],
            gender = data["gender"],
            phone_number = data["phone_number"],
            date_of_birth = date_of_birth,
            location = data["location"],
            school_type = data["school_type"],
            school = data["school"],
            occupation = data["occupation"],
            visitor = data["visitor"],
            leaders = data["leaders"],
            ag_group_id = data["ag_group_id"],
        )

        # Getting the contacts of a member and appending them to the new member
        contacts = data.get("contacts", [])
        # looping through the contacts1 and appending them to the new member
        for contact in contacts:
            contact_data = Contact(
                name = contact.get("name"),
                phone_number= contact.get("phone_number"),
                relationship = contact.get("relationship"),
                member_id = contact.get("new_member.id"))
            # appending the image_data to the new member
            new_member.contacts.append(contact_data)
        
        if new_member:
            # adding and commiting the new member to the database 
            db.session.add(new_member)
            db.session.commit()

            # creating the new member to a dictionary
            new_member_dict = new_member.to_dict()

            # creating and returning a respnse using the new_member_dict
            response = make_response(new_member_dict, 201)
            return response
        else:
            response_body = {"message": "Some field is missing"}
            response = make_response(response_body, 400)
            return response
        
    pass

#  creating a MemberById Resource
class MemberById(Resource):
    # a get method to get a member with a specific id
    def get(self, id):
        # querying and filtering the Member model using the id
        member = Member.query.filter_by(id=id).first()
        if member:
            # converting the member to a dictionary format
            member_to_dict = member.to_dict(rules=("-ag_group",))
            #  creating and returning a respose 
            response = make_response(member_to_dict, 200)
            return response
        else:
            # creating and returning a response based on the respnse body
            response_body = {"Message":f"Member with the id of {id} is not found"}
            response = make_response(response_body, 400)
            return response
        
    # a patch method to update a member with a specific id
    def patch(self, id):
        # querying and filtering the Member model using the id
        member = Member.query.filter_by(id=id).first()
        
        if member:
            # getting the data based on the request
            data = request.get_json()

            # updating the data using the setattr
            for attr in data:
                setattr(member, attr, data[attr])
            
            # commiting the member to the database
            db.session.commit()

            # converting the member to a dictionary
            member_dict = member.to_dict()

            #  creating and returning a response
            response = make_response(member_dict, 200)
            return response
        else :
            # creating and returning a response based on the respnse body
            response_body = {"Message":f"Member with the id of {id} is not found"}
            response = make_response(response_body, 400)
            return response
        
    # a method to delete the member
    def delete(self, id):
        # querying and filtering the database using the id
        member1 = Member.query.filter_by(id = id).first()
        if member1:
            #  deleting the member1 and commiting the changes to the database
            db.session.delete(member1)
            db.session.commit()
            #  creating and returning a response based on the response body
            response_body = {"message":"user deleted successfully"}
            response = make_response(response_body, 204)
            return response
        else:
            #  creating and returning a response based on the response body
            response_body = {"error": "user not found"}
            response = make_response(response_body, 404)
            return response

    pass

api.add_resource(Home, "/", endpoint="home")
api.add_resource(Members, "/members", endpoint="members")
api.add_resource(MemberById, "/members/<int:id>", endpoint="member_by_id")