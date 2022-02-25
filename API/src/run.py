import datetime
import os
from dotenv import load_dotenv

load_dotenv()

from flask import jsonify, request

# custom imports
from app import db, create_app
from models.RecipeModel import RecipeModel, RecipeSchema
from models.UserModel import UserModel, UserSchema

# create and configure the flask app
env_name = os.environ.get("FLASK_ENV")
app = create_app(env_name)


"""
ROUTES SECTION
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
def get_all_users():
    users = UserModel.get_all()
    serializer = UserSchema(many=True)
    data = serializer.dump(users)
    return jsonify(data)


@app.route("/user/<int:id>", methods=["GET"])
def get_user(id):
    recipe = UserModel.get_by_id(id)
    serializer = RecipeSchema()
    data = serializer.dump(recipe)

    return jsonify(data), 200


@app.route("/user", methods=["POST"])
def add_user():
    data = request.get_json()
    user = UserModel(
        name=data.get("name"),
        email=data.get("email"),
        password=data.get("password"),
        modified_at=datetime.datetime.utcnow(),
    )
    user.save()
    serializer = RecipeSchema()
    data = serializer.dump(user)

    return jsonify(data), 201


@app.route("/user/<int:id>", methods=["PUT"])
def update_recipe(id):
    user = UserModel.get_by_id(id)
    data = request.get_json()
    user.name = data.get("name") if data.get("name") else user.name
    user.email = data.get("email") if data.get("email") else user.email
    user.password = data.get("password") if data.get("password") else user.password
    user.modified_at = datetime.datetime.utcnow()

    db.session.commit()
    serializer = RecipeSchema()
    recipe_data = serializer.dump(data)

    return jsonify(recipe_data), 200


@app.route("/user/<int:id>", methods=["DELETE"])
def delete_user(id):
    try:
        user = UserModel.get_by_id(id)
        user.delete()
        return jsonify({"Message": "Deleted"}), 204
    except Exception as e:
        return jsonify({"Error": e}), 500


# ROUTE: Index
@app.route("/")
def home():
    return jsonify("Hello world")


if __name__ == "__main__":
    app.run()  # run app
