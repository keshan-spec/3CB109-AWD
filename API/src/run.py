import datetime
import os, jwt
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

load_dotenv()

from flask import jsonify, make_response, request

# custom imports
from app import db, create_app, bcrypt
from models.RecipeModel import RecipeModel, RecipeSchema
from models.UserModel import UserModel, UserSchema
from decorators import token_required

# create and configure the flask app
env_name = os.environ.get("FLASK_ENV")
app = create_app(env_name)


"""
ROUTES SECTION: Below are all the routes/endpoints for the API
Sub routes: /auth, /users,
"""
# ROUTES: Error Handles
@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "Resource not found"}), 404


@app.errorhandler(500)
def internal_server(error):
    return jsonify({"message": "There is a problem"}), 500


# ROUTES: Users
@app.route("/users", methods=["GET"])
@token_required
def get_all_users(_):
    """
    Get all user records"""
    users = UserModel.get_all()
    serializer = UserSchema(many=True)
    data = serializer.dump(users)
    return jsonify(data)


@app.route("/user/<int:id>", methods=["GET"])
@token_required
def get_user(_, id):
    """
    Get a user record
    @params: id"""
    recipe = UserModel.get_by_id(id)
    serializer = UserSchema()
    data = serializer.dump(recipe)

    return jsonify(data), 200


@app.route("/user/<int:id>", methods=["PUT"])
@token_required
def update_user(current_user, id):
    """
    Update a user record
    @params: id"""

    user = UserModel.get_by_id(id)
    print(user, current_user)
    if user.id != current_user.id:
        return jsonify({"message": "Unauthorized action"}), 401
    data = request.get_json()
    user.name = data.get("name") if data.get("name") else user.name
    user.email = data.get("email") if data.get("email") else user.email
    user.password = data.get("password") if data.get("password") else user.password
    user.modified_at = datetime.datetime.utcnow()

    db.session.commit()
    serializer = UserSchema()
    recipe_data = serializer.dump(data)

    return jsonify(recipe_data), 200


@app.route("/user/<int:id>", methods=["DELETE"])
@token_required
def delete_user(current_user, id):
    """
    Delete a user record
    @params: id"""
    try:
        user = UserModel.get_by_id(id)
        user.delete()
        return jsonify({"Message": f"User with ID<{id}> deleted"}), 204
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        return jsonify({"Error": error}), 500
    except Exception as e:
        return jsonify({"Error": str(e)}), 401


# ROUTES: Auth
@app.route("/login", methods=["POST"])
def login():
    # creates dictionary of form data
    auth = request.form

    if not auth or not auth.get("email") or not auth.get("password"):
        # returns 401 if any email or / and password is missing
        return make_response(
            "Could not verify",
            401,
            {"WWW-Authenticate": "Credentials Missing"},
        )

    user = UserModel.query.filter_by(email=auth.get("email")).first()

    if not user:
        # returns 401 if user does not exist
        return (
            jsonify({"ERROR": f"Could not find user with email : {auth.get('email')}"}),
            401,
        )

    try:
        valid, status = user.check_hash(auth.get("password"))
        if valid:
            # generates the JWT Token
            token = jwt.encode(
                {
                    "id": user.id,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                },
                os.environ.get("JWT_SECRET_KEY"),
            )

            return make_response(jsonify({"token": token}), 201)

        # returns 403 if password is wrong
        return make_response(
            f"Could not verify - {status}",
            403,
            {"WWW-Authenticate": status},
        )
    except Exception as e:
        return make_response(
            f"Could not verify - {e}",
            401,
            {"WWW-Authenticate": e},
        )


@app.route("/register", methods=["POST"])
def register():
    """
    Create a new user record
    @params: UserModel
        :- name
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
        name=data.get("name"),
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


# ROUTE: Index
@app.route("/")
def home():
    return jsonify("Hello world")


if __name__ == "__main__":
    app.run()  # run app
