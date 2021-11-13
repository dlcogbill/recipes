from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app

class Recipe:
    db = 'users_recipes_schema' # Name of the database/schema you'll use - class variable
    # Model for the recipe
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.madeon = data['madeon']
        self.under30 = data['under30']
        self.user_id = data['user_id']
        self.createdon = data['createdon']
        self.updatedon = data['updatedon']

    # Create a new recipe
    @classmethod
    def create_one(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, madeon, under30, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(madeon)s, %(under30)s, %(user_id)s);"
        # Need the name of the schema in the connectToMySQL statemet
        return connectToMySQL(cls.db).query_db(query, data) # Returns an integer

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True # we assume this is true
        if len(recipe['name']) < 3:
            flash('Name must be at least 3 characters.','Recipe')
            is_valid = False
        if len(recipe['description']) < 3:
            flash('Description must be at least 3 characters.','Recipe')
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash('Instructions must be at least 3 characters.','Recipe')
            is_valid = False
        
        return is_valid

    # Show one recipe from the data base
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        recipe_from_db = connectToMySQL(cls.db).query_db(query, data)
        
        return cls(recipe_from_db[0]) # Convert this item into a class instance, and return it

    # Show all Recipes
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;" # Grab a list of dictionaries, where each dictionary is a row from the DB
        recipes_from_db = connectToMySQL(cls.db).query_db(query)
        
        recipes = [] # List that will hold CLASS objects
        
        for recipe in recipes_from_db:
            recipes.append(recipe) # cls(data) makes an instance of a class
        
        return recipes

    # Edit recipe from the data base
    @classmethod
    def edit_one(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, madeon=%(madeon)s, under30=%(under30)s, user_id=%(user_id)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    # Delete recipe from the data base
    @classmethod
    def delete_one(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)