from flask import Blueprint, make_response, request
from models import db, AgGroup
from flask_restful import Resource, Api

ag_group = Blueprint("ag_group", __name__)
api = Api(ag_group)

# creating an AgGroups Resource
class AgGroups(Resource):
    # a get method to get all the ag_groups
    def get(self):
        # querying the database to get all the ag_groups
        ag_groups = AgGroup.query.all()
        # getting one ag_group and converting it to a dictionary
        ag_group_dict = [ag_group.to_dict() for ag_group in ag_groups]
        # creating and returning a response 
        response = make_response(ag_group_dict, 200)
        return response
    
    # a post method to post new ag_groups
    def post(self):
        #  getting the data based on the users request
        data = request.get_json()

        # creating a new ag_group
        new_ag_group = AgGroup(
            name = data["name"]
        )

        if new_ag_group:
            # adding and commiting the ag_group to the database 
            db.session.add(new_ag_group)
            db.session.commit()

            # converting the new_ag_group to a dictionary 
            new_ag_group_dict = new_ag_group.to_dict()
            # creating and returning a response 
            response = make_response(new_ag_group_dict, 201)
            return response
        else:
            # creating and returning a response based on the response_body 
            response_body = {"message": f"The field name is missing"}
            response = make_response(response_body, 400)
            return response
    pass

#  creating an AgGroupsById resource
class AgGroupsById(Resource):
    #  a get method to get a single ag_group by the id
    def get(self, id):
        # querying and filtering the database using the id
        ag_group=AgGroup.query.filter_by(id = id).first()

        if ag_group:
            # making the ag_group to a dictionary
            ag_group_dict = ag_group.to_dict()
            # creating and returning a response
            response = make_response(ag_group_dict, 200)
            return response
        else:
            # creating and returning a response based on the response_body
            response_body = {"message":f"The Ag Group with the id of {id} is not found"}
            response = make_response(response_body, 400)
            return response
    
    # a patch method to update the ag_group
    def patch(self,  id):
        # querying and filtering the data using the id
        ag_group = AgGroup.query.filter_by(id=id).first()
        if ag_group:
            # getting the data based on the request
            data = request.get_json()

            # setting the attribute based on the data
            for attr in data:
                setattr(ag_group, attr, data[attr])

            # commiting the ag_group to the database 
            db.session.commit()

            # making the ag_group to a dictionary
            ag_group_dict = ag_group.to_dict()

            # creating and returning a respose 
            response = make_response(ag_group_dict, 200)
            return response
        else:
            # creating and returning a response based on the response body
            response_body = {"message":f"The Ag Group with the id of {id} is not found"}
            response = make_response(response_body, 400)
            return response
    
    #  a delete method to delete the ag_group
    def delete(self, id):
        # querying and filtering the data using the id 
        ag_group = AgGroup.query.filter_by(id=id).first()
        if ag_group:
            #  deleting the ag_group and commiting it to the database 
            db.session.delete(ag_group)
            db.session.commit()

            #  creating and returnig the response based on the response body
            response_body = {"message":f"The Ag group with the id of {id} has been deleted successfully"}
            response= make_response(response_body, 204)
            return response
        else:
            # creating and returning a response based on the response body
            response_body = {"message":f"The Ag Group with the id of {id} is not found"}
            response = make_response(response_body, 400)
            return response
    pass

api.add_resource(AgGroups, "/ag-groups", endpoint="ag_groups")
api.add_resource(AgGroupsById,"/ag-groups/<int:id>", endpoint="ag_groups_by_id")