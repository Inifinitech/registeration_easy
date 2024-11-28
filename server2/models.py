from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy


#  initializing metadata and adding it to the db
metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

# creating a model called Member with a members tablename
class Member(db.Model, SerializerMixin):
    __tablename__ ="members"

    # creating columns for the members table
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    surname = db.Column(db.String(), nullable=True)
    gender = db.Column(db.String(), nullable=False)
    phone_number = db.Column(db.String(), nullable=False)
    date_of_birth = db.Column(db.DateTime(), nullable=True)
    location = db.Column(db.String(), nullable=False)
    school_type = db.Column(db.String(), nullable=False)
    school = db.Column(db.String(), nullable=False)
    occupation = db.Column(db.String(), nullable=False)
    visitor = db.Column(db.String(), nullable=False)
    leaders = db.Column(db.String(), nullable=False)
    #  foreign key from the ag_group_id
    ag_group_id = db.Column(db.Integer, db.ForeignKey("ag_groups.id"))

    #  a relationship that maps member to the related contacts
    contacts = db.relationship("Contact", back_populates="member", cascade = "all, delete-orphan")

    #  a relationship that maps member to the related ag_group
    ag_group = db.relationship("AgGroup", back_populates="member")

    # a relationship that maps the member to a related attendance 
    attendances = db.relationship("Attendance", back_populates="member", cascade = "all, delete-orphan")

    # creating serialiation rules
    serialize_rules = ("-contacts.member", "ag_group.member","-attendances.member", )

    # validating members phone_number to be exactly 10 digits
    @validates("phone_number")
    def validates_phone_number(self, key, value):
        value = str(value)
        if not value or len(value) != 10 or not value.isdigit():
            raise ValueError("The phone_number must have 10 digits")
        else:
            return value

    #  creating a string representation of the model above
    def __repr__(self):
        return f"Member {self.id}: {self.first_name}, {self.last_name}, {self.gender} {self.phone_number} has been created"

# creating a model called Contact with a contacts tablename
class Contact(db.Model, SerializerMixin):
    __tablename__ ="contacts"

    # creating columns for the contacts table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    phone_number = db.Column(db.String(), nullable=False)
    relationship = db.Column(db.String(), nullable=False)
    # foreign key from the member_id
    member_id = db.Column(db.Integer(), db.ForeignKey("members.id"))

    #  a relationship that maps  a related contacts to a member
    member = db.relationship("Member", back_populates="contacts")

    # creating serialiation rules
    serialize_rules = ("-member.contacts", )

    # validating contacts phone_number to be exactly 10 digits
    @validates("phone_number")
    def validates_phone_number(self, key, value):
        value = str(value)
        if not value or len(value) != 10 or not value.isdigit():
            raise ValueError("The phone_number must have 10 digits")
        else:
            return value
        
    #  creating a string representation of the model above
    def __repr__(self):
        return f"Contact {self.id}: {self.name}, {self.relationship}, {self.phone_number} has been created"
    
# creating a model called AgGroup with a table called ag_groups
class AgGroup(db.Model, SerializerMixin):
    __tablename__ = "ag_groups"

    # creating columns for the ag_groups table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    #  a relationship that maps  a related ag_group to a member
    member = db.relationship("Member", uselist = False , back_populates="ag_group", cascade ="all, delete-orphan")


    # creating serialiation rules
    serialize_rules = ("-member.ag_group",  )

    #  creating a string representation of the model above
    def __repr__(self):
        return f"AgGroup {self.id}: {self.name} has been created"
    
#  creating a model called Attendance with a table called attendances
class Attendance(db.Model, SerializerMixin):
    __tablename__ = "attendances"

    # creating columns for the attendances table
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(), nullable=False)
    status = db.Column(db.String(), nullable=False)
    # foreign key from the members_id
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"))

    # a relationship that maps the attendance to a related member 
    member = db.relationship("Member", back_populates="attendances")

    # creating a string representation of the model above
    def __repr__(self):
        return f"Attendance {self.id}: {self.date}, {self.status} has been created"

#  creating a model called Event with a tablename of events
class Event(db.Model, SerializerMixin):
    __tablename__ = "events"

    # creating columns for the events table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    # creating a string representation of the model above
    def __repr__(self):
        return f"Event {self.id}: {self.name} has been created"
