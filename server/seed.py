import random
from app import app
from models import db, Group, Attendance, Member, Event, MemberEvent, Admin, EmergencyContact
from faker import Faker
from datetime import datetime, timedelta
from sqlalchemy import text

fake = Faker()

# def church_events():
#     events = [
#         "Family Gathering",
#         "Community Worship",
#         "Prayer Service",
#         "Bible Study",
#         "Youth Retreat",
#         "Charity Bake Sale",
#         "Praise Concert",
#         "Volunteer Day",
#         "Harvest Festival",
#         "Mission Trip Fundraiser",
#     ]
#     return random.choice(events)

# def clear_database():
#     try:
#         print('Clearing database...')
#         MemberEvent.query.delete()
#         Attendance.query.delete()
#         Member.query.delete()
#         Event.query.delete()
#         Group.query.delete()
#         Admin.query.delete()
#         EmergencyContact.query.delete()  # Ensure emergency contacts are deleted
        
#         db.session.commit()

#         # Resetting sequences for PostgreSQL
#         sequences = {
#             'member_id_seq': "ALTER SEQUENCE member_id_seq RESTART WITH 1;",
#             'attendance_id_seq': "ALTER SEQUENCE attendance_id_seq RESTART WITH 1;",
#             'event_id_seq': "ALTER SEQUENCE event_id_seq RESTART WITH 1;"
#         }
        
#         for seq_name, command in sequences.items():
#             try:
#                 db.session.execute(text(command))
#             except Exception as e:
#                 print(f"Could not reset {seq_name}: {e}")
        
#         db.session.commit()
#         print('Database cleared and sequences reset.')
#     except Exception as e:
#         print(f"Error clearing database: {e}")
#         db.session.rollback()


def seed_groups(group_names):
    print("Seeding groups...")
    try:
        groups = [Group(name=name) for name in group_names]
        db.session.add_all(groups)
        db.session.commit()
        print(f"Seeded {len(groups)} groups.")
    except Exception as e:
        print(f"Error seeding groups: {e}")
        db.session.rollback()

# def seed_members(num_members, groups):
#     print("Seeding members...")
#     try:
#         members = []
#         genders = ['Male', 'Female']  # List of possible genders
#         for _ in range(num_members):
#             dob_string = fake.date_of_birth(minimum_age=10, maximum_age=60).isoformat()
#             dob_date = datetime.strptime(dob_string, '%Y-%m-%d').date()  # Convert string to date
            
#             # Choose a random emergency contact for the member
#             # emergency_contact = random.choice(emergency_contacts)

#             member = Member(
#                 first_name=fake.first_name(),
#                 last_name=fake.last_name(),
#                 gender_enum=random.choice(genders),  # Assign gender
#                 dob=dob_date,  # Pass the `date` object
#                 location=fake.city(),
#                 phone=fake.phone_number(),
#                 is_student=fake.boolean(chance_of_getting_true=50),
#                 will_be_coming=fake.boolean(chance_of_getting_true=50),
#                 is_visitor=fake.boolean(chance_of_getting_true=50),
#                 school=fake.company() if random.choice([True, False]) else None,  # Randomize presence of school
#                 occupation=fake.job(),
#                 group_id=random.choice(groups).id,
#                 # emergency_contact_id=emergency_contact.id  # Link to emergency contact
#             )
#             members.append(member)

#         db.session.add_all(members)
#         db.session.commit()
#         print(f"Seeded {len(members)} members.")
#         return members
#     except Exception as e:
#         print(f"Error seeding members: {e}")
#         db.session.rollback()
#         return []
    
# # def seed_emergency_contacts(num_contacts):
# #     print("Seeding emergency contacts...")
# #     try:
# #         contacts = [
# #             EmergencyContact(
# #                 name=fake.name(),
# #                 phone=fake.phone_number(),
# #                 relation=random.choice(["Parent", "Sibling", "Spouse", "Friend", "Guardian"])
# #             )
# #             for _ in range(num_contacts)
# #         ]
# #         db.session.add_all(contacts)
# #         db.session.commit()
# #         print(f"Seeded {len(contacts)} emergency contacts.")
# #         return contacts
# #     except Exception as e:
# #         print(f"Error seeding emergency contacts: {e}")
# #         db.session.rollback()
# #         return []

# def prepare_attendance_data(members, date="2024-11-10"):
#     # Create a list of attendance records with member_id, status, and date
#     return [
#         {
#             "member_id": member.id,  # Use the Member object's attributes directly
#             "status": random.choice(["present", "absent"]),
#             "date": date,  # Use the given date or customize it
#         }
#         for member in members
#     ]

# def seed_attendance(attendances):
#     print("Seeding attendance...")
#     try:
#         attendance_records = []
#         for attendance in attendances:
#             # Ensure each attendance entry is processed correctly as a dictionary
#             attendance_records.append(
#                 Attendance(
#                     member_id=attendance["member_id"],  # Access member_id from dictionary
#                     status=attendance["status"],
#                     date=datetime.strptime(attendance["date"], "%Y-%m-%d").date()  # Ensure date is a Python date object
#                 )
#             )

#         db.session.add_all(attendance_records)
#         db.session.commit()
#         print(f"Seeded {len(attendance_records)} attendance records.")
#         return attendance_records

#     except Exception as e:
#         print(f"Error seeding attendance: {e}")
#         db.session.rollback()
#         return []

# def seed_events(num_events):
#     print("Seeding events...")
#     try:
#         events = [Event(name=church_events()) for _ in range(num_events)]
#         db.session.add_all(events)
#         db.session.commit()
#         print(f"Seeded {len(events)} events.")
#         return events
#     except Exception as e:
#         print(f"Error seeding events: {e}")
#         db.session.rollback()
#         return []

# def seed_member_events(members, events):
#     print("Seeding member events...")
#     try:
#         memberevents = [
#             MemberEvent(
#                 member_id=random.choice(members).id,
#                 event_id=random.choice(events).id
#             ) for _ in range(50)
#         ]
#         db.session.add_all(memberevents)
#         db.session.commit()
#         print(f"Seeded {len(memberevents)} member events.")
#     except Exception as e:
#         print(f"Error seeding member events: {e}")
#         db.session.rollback()

# def seed_admin():
#     print("Seeding admin...")
#     try:
#         user = Admin(
#             username=fake.user_name(),
#             password='tripin'  # Consider hashing passwords in production
#         )
#         db.session.add(user)
#         db.session.commit()
#         print("Admin user seeded.")
#     except Exception as e:
#         print(f"Error seeding admin: {e}")
        # db.session.rollback()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # clear_database()

        group_names = [
            "Transformers",
            "Relentless",
            "Innovators",
            "Pacesetters",
            "Ignition",
            "Gifted",
            "Visionaries",
            "Elevated"
        ]

        seed_groups(group_names)
        groups = Group.query.all() 

        # # emergency_contacts = seed_emergency_contacts(30)  # Seed emergency contacts first
        # members = seed_members(30, groups)  # Pass emergency contacts to member seeding

        # if members:
        #     attendance_data = prepare_attendance_data(members)  # Prepare attendance data
        #     seed_attendance(attendance_data)  # Seed attendance

        # events = seed_events(30)
        # if events:
        #     seed_member_events(members, events)

        # seed_admin()
