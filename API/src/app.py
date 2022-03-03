# src/app.py
import datetime
from flask import Flask, jsonify
from models.EventModel import EventModel
from models.WorkPlace import WorkPlaceModel
from models.UserModel import UserModel
from config import app_config
from models import db, bcrypt  # add this new line


def create_app(env_name):
    # app initiliazation
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])

    # initializing bcrypt
    bcrypt.init_app(app)  # add this line
    db.init_app(app)  # add this line

    return app


def fill_tables():
    # create test users
    users = [
        {
            "fname": "Shehan",
            "lname": "Jude",
            "email": "shehan@ysjcs.net",
            "password": "123",
        },
        {
            "fname": "Keshanth",
            "lname": "Jude",
            "email": "keshan@ysjcs.net",
            "password": "123",
        },
        {
            "fname": "Jathusa",
            "lname": "Thiruchelvam",
            "email": "jathu@ysjcs.net",
            "password": "123",
        },
        {
            "fname": "Sharaf",
            "lname": "Mohamed",
            "email": "sharaf@ysjcs.net",
            "password": "123",
        },
        {
            "fname": "Shavin",
            "lname": "Supramanium",
            "email": "shavin@ysjcs.net",
            "password": "123",
        },
        {
            "fname": "Shopikar",
            "lname": "Supramanium",
            "email": "shopi@ysjcs.net",
            "password": "123",
        },
    ]

    for user in users:
        try:
            user = UserModel(
                fname=user["fname"],
                lname=user["lname"],
                email=user["email"],
                password=user["password"],
                modified_at=datetime.datetime.utcnow(),
            )
            user.password = user.generate_hash(user.password)
            user.save()
        except Exception as e:
            print("ERROR: ", e)
            break

    print("CREATED TEST DATA: Users")

    # create test workplaces
    workplaces = [
        {
            "name": "SPAR Tanghall",
            "location": "Tanghall Lane, YO10 3RA, York, UK",
            "user_id": 1,
            "joined_on": datetime.datetime.utcnow(),
        },
        {
            "name": "SPAR Bridgetreet",
            "location": "17 Bridgestreet, YO10 3RA, York, UK",
            "user_id": 1,
            "joined_on": datetime.datetime.utcnow(),
        },
    ]

    for workplace in workplaces:
        try:
            workplace = WorkPlaceModel(
                name=workplace["name"],
                location=workplace["location"],
                user_id=workplace["user_id"],
                joined_on=workplace["joined_on"],
            )
            workplace.save()
        except Exception as e:
            print("ERROR: ", e)
            break

    print("CREATED TEST DATA: WorkPlaces")

    # create test events
    events = [
        {
            "name": "Event 1",
            "description": "This is the first event",
            "start": datetime.datetime.utcnow(),
            "finish": datetime.datetime.utcnow(),
            "repeat": "Never",
            "work_id": 1,
            "user_id": 1,
        }
    ]

    for event in events:
        try:
            event = EventModel(
                name=event["name"],
                description=event["description"],
                start=event["start"],
                finish=event["finish"],
                repeat=event["repeat"],
                work_id=event["work_id"],
                user_id=event["user_id"],
            )
            event.save()
        except Exception as e:
            print("ERROR: ", e)
            break

    print("CREATED TEST DATA: Events")


if __name__ == "__main__":
    app = create_app("development")
    with app.app_context():
        try:
            print("Droping all tables")
            db.drop_all()
            db.create_all()
            print("Database tables created")
            fill_tables()  # create dummy data
        except AttributeError as e:
            print(f"Error: {e}")
