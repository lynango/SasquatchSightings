from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Sighting:
    db_name = "sasquatch_sightings"

    def __init__(self,db_data):
        self.id = db_data['id']
        self.location = db_data['location']
        self.what_happened = db_data['what_happened']
        self.date_of_sighting = db_data['date_of_sighting']
        self.num_of_sasquatches = db_data['num_of_sasquatches']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.reporter = db_data['reporter']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sightings;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        sightings = []
        for new_row in results:
            sightings.append( cls(new_row) )
            print(new_row['date_of_sighting'])
        return sightings 

    @classmethod
    def save(cls,data):
        query = "INSERT INTO sightings (location, what_happened, date_of_sighting, num_of_sasquatches, reporter, user_id) VALUES (%(location)s,%(what_happened)s,%(date_of_sighting)s,%(num_of_sasquatches)s,%(reporter)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM sightings WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def get_all_with_reporter (cls):
        query = "SELECT * FROM sightings LEFT JOIN users ON sightings.user_id = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results)
        all_sightings = []
        for one_sighting in results:
            sighting_data = {
                "id": one_sighting['id'],
                "location": one_sighting['location'],
                "what_happened": one_sighting['what_happened'],
                "date_of_sighting": one_sighting['date_of_sighting'],
                "num_of_sasquatches": one_sighting['num_of_sasquatches'],
                "reporter": one_sighting['reporter'],
                "created_at": one_sighting['created_at'],
                "updated_at": one_sighting['updated_at']
            }
            sighting_object = cls(sighting_data)
            user_data = {
                "id": one_sighting['users.id'],
                "first_name": one_sighting['first_name'],
                "last_name": one_sighting['last_name'],
                "email": one_sighting['email'],
                "password": one_sighting['password'],
                "created_at": one_sighting['users.created_at'],
                "updated_at": one_sighting['users.updated_at']
            }
            single_user = user.User(user_data)
            sighting_object.reporter = single_user
            all_sightings.append(sighting_object)
        return results

    @classmethod
    def update(cls, data):
        query = "UPDATE sightings SET location=%(location)s, what_happened=%(what_happened)s, date_of_sighting=%(date_of_sighting)s, num_of_sasquatches=%(num_of_sasquatches)s, reporter=%(reporter)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM sightings WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_sighting_report(sighting):
        is_valid = True
        if len(sighting['location']) < 3:
            is_valid = False
            flash("The location must be at least 3 characters", "sighting")
        if len(sighting['what_happened']) < 3:
            is_valid = False
            flash("Description must be at least 3 character", "sighting")
        if int(sighting['num_of_sasquatches']) <= 0:
            is_valid = False
            flash("You cannot report a sighting without seeing a sasquatch. Please enter the number of sasquatches you saw.", "sighting")
        if sighting['date_of_sighting'] == "": 
            is_valid = False
            flash("Please enter the date of sighting", "sighting")
        return is_valid
