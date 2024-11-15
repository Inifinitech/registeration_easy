import random
from app import app
from models import db, Group, Attendance, Member, Event, MemberEvent, Admin
from faker import Faker
from datetime import datetime, timedelta
from sqlalchemy import text

fake = Faker()

def church_events():
    events = [
        "Family Gathering",
        "Community Worship",
        "Prayer Service",
        "Bible Study",
        "Youth Retreat",
        "Charity Bake Sale",
        "Praise Concert",
        "Volunteer Day",
        "Harvest Festival",
        "Mission Trip Fundraiser",
    ]
    return random.choice(events)

def clear_database():
    try:
        print('Clearing database...')
        MemberEvent.query.delete()
        Attendance.query.delete()
        Member.query.delete()
        Event.query.delete()
        Group.query.delete()
        Admin.query.delete()
        
        db.session.commit()

        # Resetting sequences for PostgreSQL
        sequences = {
            'member_id_seq': "ALTER SEQUENCE member_id_seq RESTART WITH 1;",
            'attendance_id_seq': "ALTER SEQUENCE attendance_id_seq RESTART WITH 1;",
            'event_id_seq': "ALTER SEQUENCE event_id_seq RESTART WITH 1;"
        }
        
        for seq_name, command in sequences.items():
            try:
                db.session.execute(text(command))
            except Exception as e:
                print(f"Could not reset {seq_name}: {e}")
        
        db.session.commit()
        print('Database cleared and sequences reset.')
    except Exception as e:
        print(f"Error clearing database: {e}")
        db.session.rollback()


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

def seed_members(num_members, groups):
    print("Seeding members...")
    try:
        members = []
        genders = ['Male', 'Female']  # List of possible genders
        for _ in range(num_members):
            member = Member(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                gender_enum=random.choice(genders),  # Assign gender
                dob=fake.date_of_birth(minimum_age=10, maximum_age=60).isoformat(),  # Use ISO format for date
                location=fake.city(),
                phone=fake.phone_number(),
                is_student=fake.boolean(chance_of_getting_true=50),
                will_be_coming=fake.boolean(chance_of_getting_true=50),
                is_visitor=fake.boolean(chance_of_getting_true=50),
                school=fake.company() if random.choice([True, False]) else None,  # Randomize presence of school
                occupation=fake.job(),
                group_id=random.choice(groups).id
            )
            members.append(member)

        db.session.add_all(members)
        db.session.commit()
        print(f"Seeded {len(members)} members.")
        return members
    except Exception as e:
        print(f"Error seeding members: {e}")
        db.session.rollback()
        return []



def seed_attendance(members):
    print("Seeding attendances...")
    try:
        today = datetime.now()
        sunday_date = today - timedelta(days=(today.weekday() + 1) % 7)
        attendance_date = sunday_date.strftime('%Y-%m-%d')

        attendances = [
            Attendance(
                date=attendance_date,
                status=random.choice(['present', 'absent']),
                member_id=random.choice(members).id
            ) for _ in range(20)
        ]
        db.session.add_all(attendances)
        db.session.commit()
        print(f"Seeded {len(attendances)} attendance records.")
    except Exception as e:
        print(f"Error seeding attendance: {e}")
        db.session.rollback()

def seed_events(num_events):
    print("Seeding events...")
    try:
        events = [Event(name=church_events()) for _ in range(num_events)]
        db.session.add_all(events)
        db.session.commit()
        print(f"Seeded {len(events)} events.")
        return events
    except Exception as e:
        print(f"Error seeding events: {e}")
        db.session.rollback()
        return []

def seed_member_events(members, events):
    print("Seeding member events...")
    try:
        memberevents = [
            MemberEvent(
                member_id=random.choice(members).id,
                event_id=random.choice(events).id
            ) for _ in range(50)
        ]
        db.session.add_all(memberevents)
        db.session.commit()
        print(f"Seeded {len(memberevents)} member events.")
    except Exception as e:
        print(f"Error seeding member events: {e}")
        db.session.rollback()

def seed_admin():
    print("Seeding admin...")
    try:
        user = Admin(
            username=fake.user_name(),
            password='tripin'  # Consider hashing passwords in production
        )
        db.session.add(user)
        db.session.commit()
        print("Admin user seeded.")
    except Exception as e:
        print(f"Error seeding admin: {e}")
        db.session.rollback()

if __name__ == '__main__':
    with app.app_context():
        clear_database()

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

        members = seed_members(30, groups)
        if members:
            seed_attendance(members)

        events = seed_events(30)
        if events:
            seed_member_events(members, events)

        seed_admin()
