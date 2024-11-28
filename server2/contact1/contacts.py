from models import Contact,db
from flask import Blueprint, make_response, request
from flask_restful import Api, Resource

contacts = Blueprint("contacts", __name__)
api = Api(contacts)

#  creating a Contacts Resource
class Contacts(Resource):
    # creating a get method that gets all contacts
    def get(self):
        # Querying the database to get all the contacts
        contacts = Contact.query.all()
        # Looping through all contacts to get one contact in a dictionary form of display
        contact1 = [contact.to_dict() for contact in contacts]
        # creating and returning a response 
        response = make_response(contact1, 200)
        return response
    
    #  creating a method to post new contacts
    def post(self):
        #  creating a new contact out of the users input
        data =request.get_json()
        
        new_contact = Contact(
            name = data["name"],
            phone_number = data["phone_number"],
            relationship = data["relationship"],
            member_id = data["member_id"]
        )

        if new_contact:
            # adding and commiting the new member to the database 
            db.session.add(new_contact)
            db.session.commit()

            # creating the new member to a dictionary
            new_contact_dict = new_contact.to_dict()

            # creating and returning a respnse using the new_contact_dict
            response = make_response(new_contact_dict, 201)
            return response
        else:
            response_body = {"message": "Some field is missing"}
            response = make_response(response_body, 400)
            return response
        
    pass

api.add_resource(Contacts, "/contacts", endpoint="contacts")


