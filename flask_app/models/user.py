from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re # The regex module; A package for regular expressions. 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[A-Z][-a-zA-Z]+$')

from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)

class User:
    db_name = "sasquatch_sightings"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.sightings = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for new_row in results:
            users.append( cls(new_row) )
        return users

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        print(results)
        return results

    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        print(results)
        return cls(results[0])

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        print(results)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])


    @staticmethod
    def registration(user):
        is_valid = True
        users_with_email = User.get_by_email({"email": user['email']})
        print(users_with_email)
        if users_with_email:
            flash("Email has already been used")
            is_valid=False
        if not NAME_REGEX.match(user['first_name']) or not NAME_REGEX.match(user['last_name']):
            flash("Invalid first or last name")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address/password")
            is_valid=False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters")
            is_valid= False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid= False
        if user['password'] != user['confirm']:
            flash("Password and confirm password does not match")
        return is_valid
