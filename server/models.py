from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import Enum
from sqlalchemy.dialects.sqlite import JSON
from datetime import datetime

db=SQLAlchemy()

class Group(db.Model,SerializerMixin):
    __tablename__= 'groups'
    serialize_rules=('-members.group',)
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False,unique=True)
    #one to many with Member
    members=db.relationship('Member',back_populates='group', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<id {self.id},name{self.name}>'

    
class Member(db.Model,SerializerMixin):
    __tablename__='members'
    serialize_rules=('-group.members','-attendances.member','-memberevents.member',)
    
    id=db.Column(db.Integer,primary_key=True)
    first_name=db.Column(db.String,nullable=False)
    last_name=db.Column(db.String,nullable=False)
    gender_enum = db.Column(Enum("Male", "Female", name="gender_enum"), nullable=True)
    dob=db.Column(db.Date,nullable=False)
    location = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    is_student = db.Column(db.Boolean, default=False)
    will_be_coming = db.Column(db.Boolean, default=False)
    is_visitor = db.Column(db.Boolean, default=False)
    school = db.Column(db.String, nullable=True)
    occupation = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime)
    
    group_id=db.Column(db.Integer,db.ForeignKey('groups.id'))

    memberevents=db.relationship('MemberEvent',back_populates='member')
    events=association_proxy('memberevents','eveont')
    emergency_contacts = db.relationship('EmergencyContact', back_populates='members')
    

    #one to many with Group
    group=db.relationship('Group',back_populates='members')

    #one to many with attendance/one member can have many attendances
    attendances=db.relationship('Attendance',back_populates='member',cascade="all, delete-orphan")

    def __repr__(self):
        return f'<id {self.id},first_name{self.first_name},last_name{self.last_name},dob{self.dob},location{self.location},phone{self.phone},occupation{self.occupation}>'
    
class EmergencyContact(db.Model, SerializerMixin):
    __tablename__ = 'emergency_contacts'

    serialize_rules = ('-members')
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    relation = db.Column(db.String, nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'))

    members = db.relationship('Member', back_populates='emergency_contacts')
    
    
class Attendance(db.Model,SerializerMixin):
    __tablename__='attendances'
    serialize_rules=('-member.attendances',)

    id=db.Column(db.Integer,primary_key=True)
    date=db.Column(db.Date,nullable=False)
    status=db.Column(db.String,nullable=False)

    member_id=db.Column(db.Integer,db.ForeignKey('members.id'))

    #one to many 
    member=db.relationship('Member',back_populates='attendances')

class Event(db.Model,SerializerMixin):
    __tablename__='events'
    serialize_rules=('-memberevent.event',)

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String)
    #one event many members
    #one member many events
    memberevents=db.relationship('MemberEvent',back_populates='event')
    members=association_proxy('memberevents','member')


class MemberEvent(db.Model,SerializerMixin):
    __tablename__='memberevents'
    serialize_rules=('-member.memberevents','-event.memberevents',)
    id=db.Column(db.Integer,primary_key=True)

    event_id=db.Column(db.Integer,db.ForeignKey('events.id'))
    member_id=db.Column(db.Integer,db.ForeignKey('members.id'))

    member=db.relationship('Member',back_populates='memberevents')
    event=db.relationship('Event',back_populates='memberevents')
    
class Admin(db.Model,SerializerMixin):
    __tablename__='admins'

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String)

    def __repr__(self):
        return '<user:{self.user_name}>'