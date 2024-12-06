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

# creating a ContactById Resource
class ContactById(Resource):
    # creating a get method to get the contacts based on the id 
    def get(self, id):
        #  querying and filtering the database based on the id 
        contact = Contact.query.filter_by(id=id).first()

        if contact:
            # making the contact to a dictionary
            contact_dict = contact.to_dict(rules=("-member.ag_group",))
            #  creating and returning a response 
            response = make_response(contact_dict, 200)
            return response
        else:
            # creating and returning a response based on the response body
            response_body = {"message":f"The contact with the id of {id} is not found"}
            response = make_response(response_body, 400)
            return response
    
    #  a patch method to update the details of a contact
    def patch(self, id):
        # querying and filtering the database based on the id
        contact = Contact.query.filter_by(id=id).first()

        if contact:
            # getting the data based on the request
            data = request.get_json()

            # setting the attributes based on the data
            for attr in data:
                setattr(contact, attr, data[attr])
            
            # commiting the changes to the database
            db.session.commit()

            # making the contact to a dictionary using the to_dict method
            contact_dict = contact.to_dict(rules=("-member.ag_group",))
            # creating and returning a response based on the contact dict
            response = make_response(contact_dict, 200)
            return response
        else:
            # creating and returning a response based on the response_body
            response_body = {"message":f"The contact with the id of {id} is not found"}
            response = make_response(response_body, 400)
            return response
    
    #  a method to delete the contact based on the id
    def delete(self, id):
        # querying and filtering the database based on the id
        contact = Contact.query.filter_by(id=id).first()

        if contact:
            # deleting the contact and commiting the changes to the database 
            db.session.delete(contact)
            db.session.commit()

            # creating and returning a response based on the response_body
            response_body = {"message":f"The contact with the id of {id} has been deleted successfully"}
            response = make_response(response_body, 204)
            return response
        else:
            # creating and returning a response based on the response body
            response_body = {"message":f"The contact with the id of {id} is not found"}
            response = make_response(response_body, 400)
            return response
    pass

api.add_resource(Contacts, "/contacts", endpoint="contacts")
api.add_resource(ContactById, "/contacts/<int:id>", endpoint="contact_by_id")


