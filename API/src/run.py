import os
from flask import jsonify, request

# custom imports
from app import create_app
from models.RecipeModel import Recipe, RecipeSchema

# create and configure the flask app
env_name = os.getenv("FLASK_ENV")
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
@app.route("/recipes", methods=["GET"])
def get_all_recipes():
    recipes = Recipe.get_all()
    serializer = RecipeSchema(many=True)
    data = serializer.dump(recipes)
    return jsonify(data)


@app.route("/recipes", methods=["POST"])
def create_a_recipe():
    data = request.get_json()
    new_recipe = Recipe(name=data.get("name"), description=data.get("description"))
    new_recipe.save()
    serializer = RecipeSchema()
    data = serializer.dump(new_recipe)

    return jsonify(data), 201


@app.route("/recipe/<int:id>", methods=["GET"])
def get_recipe(id):
    recipe = Recipe.get_by_id(id)
    serializer = RecipeSchema()
    data = serializer.dump(recipe)

    return jsonify(data), 200


@app.route("/recipe/<int:id>", methods=["PUT"])
def update_recipe(id):
    recipe_to_update = Recipe.get_by_id(id)
    data = request.get_json()
    recipe_to_update.name = data.get("name")
    recipe_to_update.description = data.get("description")

    db.session.commit()
    serializer = RecipeSchema()
    recipe_data = serializer.dump(recipe_to_update)

    return jsonify(recipe_data), 200


@app.route("/recipe/<int:id>", methods=["DELETE"])
def delete_recipe(id):
    recipe_to_delete = Recipe.get_by_id(id)

    recipe_to_delete.delete()

    return jsonify({"message": "Deleted"}), 204


# ROUTE: Index
incomes = [{"description": "salary", "amount": 5000}]


@app.route("/")
def home():
    return jsonify("Hello world")


@app.route("/incomes")
def get_incomes():
    return jsonify(incomes)


@app.route("/incomes", methods=["POST"])
def add_income():
    incomes.append(request.get_json())
    return "", 204


if __name__ == "__main__":

    # run app
    app.run()
