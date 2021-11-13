from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = 'users_recipes_schema' # Name of the database/schema you'll use - class variable
    # Model for the user - notice the names of the fields must match those in the DB
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Create a new user
    @classmethod
    def create_one(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        # Need the name of the schema in the connectToMySQL statemet
        return connectToMySQL(cls.db).query_db(query, data) # Returns an integer

    @staticmethod
    def validate_user(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 2:
            flash('First name must be at least 2 characters.','Registration')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Last name must be at least 2 characters.','Registration')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters.','Registration')
            is_valid = False
        if user['password'] != user['confirm']:
            flash('Passwords do not match.','Registration')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash('Invalid email address!','Registration')
            is_valid = False
        query = "SELECT * FROM users WHERE email = %(email)s;"
        
        list_of_users = connectToMySQL(User.db).query_db(query, user)
        if len(list_of_users) > 0:
            flash('Email address already exists','Registration')
            is_valid = False
        
        return is_valid
    
    @staticmethod
    def validate_login(data):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        list_of_users = connectToMySQL(User.db).query_db(query, data)

        if len(list_of_users) < 1:
            flash('Invalid Email/Password!','Login')
            is_valid = False
            return is_valid
        
        user = User(list_of_users[0])

        if not bcrypt.check_password_hash(user.password, data['password']):
            # if we get False after checking the password
            flash('Invalid Email/Password!','Login')
            is_valid = False
            return is_valid

        if is_valid:
            is_valid = user.id
        return is_valid

    # Show one User from the data base
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        user_from_db = connectToMySQL(cls.db).query_db(query, data)
        return cls(user_from_db[0]) # Convert this item into a class instance, and return it