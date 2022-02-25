# src/app.py
from flask import Flask, jsonify
from models.RecipeModel import RecipeModel
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


if __name__ == "__main__":
    app = create_app("development")
    with app.app_context():
        try:
            db.create_all()
        except AttributeError as e:
            print(f"Error: {e}")
