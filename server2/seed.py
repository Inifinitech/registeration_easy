from random import choice as rc
from faker import Faker
from app import app
from models import db, Member, Contact, AgGroup, Attendance, Event
from datetime import datetime

with app.app_context():
    db.drop_all()
    db.create_all()
    
    # Initializing Faker
    fake = Faker()

    # AgGroup names (you can adjust this list as needed)
    ag_group_names = ['Group A', 'Group B', 'Group C', 'Group D', 'Group E']

    # Event names (you can adjust this list as needed)
    event_names = ['Event 1', 'Event 2', 'Event 3', 'Event 4', 'Event 5']

    # Create AgGroup instances
    ag_groups = [
        AgGroup(name=ag_group_name) for ag_group_name in ag_group_names
    ]
    db.session.add_all(ag_groups)
    db.session.commit()

    # Create Event instances
    events = [
        Event(name=event_name) for event_name in event_names
    ]
    db.session.add_all(events)
    db.session.commit()

    # Create Member instances
    members = [
        Member(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            surname=fake.last_name(),
            gender=rc(['Male', 'Female']),
            phone_number=str(fake.random_number(digits=10)).zfill(10),  # Ensure 10 digits
            date_of_birth=fake.date_of_birth(),
            location=fake.city(),
            school_type=rc(['Public', 'Private']),
            school=fake.company(),
            occupation=fake.job(),
            visitor=rc([True, False]),
            leaders=rc([True, False]),
            ag_group_id=rc([ag_group.id for ag_group in ag_groups])  # Randomly assign ag_group
        ) for _ in range(10)  # Creating 10 members
    ]
    db.session.add_all(members)
    db.session.commit()

    # Create Contact instances
    contacts = [
        Contact(
            name=fake.name(),
            phone_number=str(fake.random_number(digits=10)).zfill(10),  # Ensure 10 digits
            relationship=rc(['Friend', 'Family', 'Colleague', 'Other']),
            member_id=rc([member.id for member in members])  # Randomly assign member
        ) for _ in range(20)  # Creating 20 contacts
    ]
    db.session.add_all(contacts)
    db.session.commit()

    # Create Attendance instances
    attendances = [
        Attendance(
            date=fake.date_this_year(),
            status=rc(['Present', 'Absent']),
            member_id=rc([member.id for member in members])  # Randomly assign member
        ) for _ in range(15)  # Creating 15 attendances
    ]
    db.session.add_all(attendances)
    db.session.commit()

    print("Database seeded successfully!")
