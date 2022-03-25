import datetime
import os, jwt
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify, request
from flask_cors import CORS, cross_origin
from flask import make_response, redirect
from dotenv import load_dotenv

load_dotenv()


# custom imports
from app import db, create_app
from models.WorkPlace import WorkPlaceModel, WorkPlaceSchema
from models.EventModel import EventSchema, EventModel
from models.UserModel import UserModel, UserSchema
from decorators import token_required

# create and configure the flask app
env_name = os.getenv("FLASK_ENV")
API_URL = "/api/v1"

app = create_app(env_name)
# api_v1_cors_config = {"origins": ["http://localhost:3001"]}
# CORS(app, resources={"/api/v1/login": api_v1_cors_config})
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


def create_token(id, exp=30):
    return jwt.encode(
        {
            "id": id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=exp),
        },
        os.environ.get("JWT_SECRET_KEY"),
    )


"""
ROUTES SECTION: Below are all the routes/endpoints for the API
Sub routes: /auth, /users, /events, /workplaces
"""
# ROUTES: Error Handles
@app.errorhandler(404)
def not_found(error):
    return jsonify({"ERROR": "Invalid route!"}), 404


@app.errorhandler(500)
def internal_server(error):
    return jsonify({"ERROR": "Internal server error!"}), 500


# ROUTES: Users
@app.route(f"{API_URL}/users", methods=["GET"])
@token_required
def get_all_users(_):
    """
    Get all user records"""
    users = UserModel.get_all()
    serializer = UserSchema(many=True)
    data = serializer.dump(users)
    return jsonify(data), 200


@app.route(f"{API_URL}/user/<int:id>", methods=["GET"])
@token_required
def get_user(_, id):
    """
    Get a user record
    @params: id"""
    users = UserModel.get_by_id(id)
    serializer = UserSchema()
    data = serializer.dump(users)

    return jsonify(data), 200


@app.route(f"{API_URL}/users/find", methods=["GET"])
@token_required
def find(_):
    """
    Find specific records"""

    users = UserModel.find(**request.get_json())
    serializer = UserSchema(many=True)
    data = serializer.dump(users)
    return jsonify(data), 200


@app.route(f"{API_URL}/user/<int:id>", methods=["PUT"])
@token_required
def update_user(current_user, id):
    """
    Update a user record
    @params: id"""

    user = UserModel.get_by_id(id)

    if user.id != current_user.id:
        return jsonify({"ERROR": "Unauthorized action"}), 401

    data = request.get_json()
    user.fname = data.get("fname") if data.get("fname") else user.fname
    user.lname = data.get("lname") if data.get("lname") else user.lname
    user.email = data.get("email") if data.get("email") else user.email
    user.password = data.get("password") if data.get("password") else user.password
    user.modified_at = datetime.datetime.utcnow()

    db.session.commit()
    serializer = UserSchema()
    updated_data = serializer.dump(data)

    return jsonify({"UPDATED": updated_data}), 200


@app.route(f"{API_URL}/user/<int:id>", methods=["DELETE"])
@token_required
def delete_user(current_user, id):
    """
    Delete a user record
    @params: id"""
    try:
        user = UserModel.get_by_id(id)
        user.delete()
        return jsonify({"message": f"{user} deleted"}), 200
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        return jsonify({"Error": error}), 500
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


# ROUTES: Auth
@app.route(f"{API_URL}/login", methods=["POST"])
@cross_origin()
def login():
    # creates dictionary of form data
    auth = request.json

    if not auth or not auth["email"] or not auth["password"]:
        # returns 401 if any email or / and password is missing
        return (jsonify({"ERROR": "Credentials missing!"}), 401)

    user = UserModel.query.filter_by(email=auth["email"]).first()
    if not user:
        # returns 401 if user does not exist
        return (
            jsonify({"ERROR": f"Could not find user with email : {auth['email']}"}),
            401,
        )

    try:
        valid, status = user.check_hash(auth["password"])
        if valid:
            # generates the JWT Token
            token = create_token(user.id)
            # set cookie on client
            # response = make_response(redirect("/"), {"token": token})
            # response.set_cookie("token", token)
            # return response
            return jsonify({"token": token}), 200

        # returns 403 if password is wrong
        return jsonify(f"Could not verify - {status}"), 403
    except Exception as e:
        return jsonify(f"Could not verify - {e}"), 403


@app.route(f"{API_URL}/register", methods=["POST"])
def register():
    """
    Create a new user record
    @params: UserModel
        :- fname
        :- lname
        :- email
        :- password
        :- created_at (default date time)
        :- modified_at (date time)
    """
    data = request.get_json()
    user = UserModel.query.filter_by(email=data.get("email")).first()

    if user:
        # returns 500 if user not exist
        return (
            jsonify({"Integreity Error": f"Email ({user.email}) already exists!"}),
            500,
        )

    user = UserModel(
        fname=data.get("fname"),
        lname=data.get("lname"),
        email=data.get("email"),
        password=data.get("password"),
        modified_at=datetime.datetime.utcnow(),
    )

    user.password = user.generate_hash(user.password)

    try:
        user.save()
        serializer = UserSchema()
        data = serializer.dump(user)
        return jsonify(data), 201
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        return jsonify({"SQLALCHEMY ERROR": error}), 500


# logout
@app.route(f"{API_URL}/logout", methods=["POST"])
@token_required
def logout(current_user):
    """
    Logout a user
    @params: id
    """
    try:
        current_user.logout(request.headers["x-access-token"])
        return jsonify({"message": "Logged out"}), 200
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


@app.route(f"{API_URL}/user/workplc", methods=["GET"])
@token_required
def get_user_workplaces(current_user):
    """
    Get the current user's workplaces
    """
    wp = WorkPlaceModel.get_by_user(current_user.id)
    if wp.count() == 0:
        return jsonify({"message": "No workplaces found"}), 400

    serializer = WorkPlaceSchema(many=True)
    data = serializer.dump(wp)
    return jsonify(data), 200


@app.route(f"{API_URL}/user/events", methods=["GET"])
@token_required
def get_user_events(current_user):
    """
    Get the current user's events
    """
    event = EventModel.get_by_user(current_user.id)

    # serialize the user data and discard the password
    user = UserSchema()
    data = user.dump(current_user)
    data.pop("password")

    # if there are no events
    if len(event) < 1:
        return jsonify({"message": "No events found"}), 400

    # serialize each work place model, remove the user_id column and add to list
    for i in range(len(event)):
        work_serializer = WorkPlaceSchema()
        _work = work_serializer.dump(event[i]["work"])
        _work.pop("user_id")
        event[i]["work"] = _work

    return jsonify({"user": data, "events": event}), 200


@app.route(f"{API_URL}/user/hours", methods=["POST"])
@token_required
def get_total_hours(current_user):
    """
    Get the total hours worked by a user
    """
    hours = EventModel.get_total_hours(current_user.id)

    return jsonify(hours), 200


# ROUTE: Index
@app.route(f"{API_URL}/")
def home():
    return jsonify("Hello world")


if __name__ == "__main__":
    app.run(port=os.getenv("YSJ_PORT"))  # run app
