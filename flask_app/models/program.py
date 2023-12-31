from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user as user_module
from flask_app.models import week as week_module

class Program:
    def __init__(self, data) -> None:
        self.id = data.get('id')
        self.title = data.get('title')
        self.description = data.get('description')
        self.user_id = data.get('user_id')
        self.owner = None # Add the user object here
        self.weeks = [] # Add week objects here

    def add_week(self, week):
        self.weeks.append(week)
    
    def get_all_weeks(self):
        self.weeks = week_module.Week.get_all_by_program_id(self.id)
        return self.weeks


    @classmethod
    def create_program(cls, data):
        # Associate the program with user at the route
        query = """
            INSERT INTO programs (
                user_id,
                title,
                description
            )
            VALUES (
                %(user_id)s,
                %(title)s,
                %(description)s
            );
        """
        return connectToMySQL('workout_tracker_schema').query_db(query, data)

    @classmethod
    def get_all_by_user_id(cls, user_id):
        query = "SELECT * FROM programs WHERE user_id = %(user_id)s;"
        data = {
            'user_id' : user_id
        }

        results = connectToMySQL('workout_tracker_schema').query_db(query, data)

        programs = []

        for row in results:
            programs.append(cls(row))
        return programs


    # Get program by id
    @classmethod
    def get_by_id(cls, program_id):
        query = "SELECT * FROM programs WHERE id = %(id)s;"

        data = {
            'id' : program_id
        }

        result = connectToMySQL('workout_tracker_schema').query_db(query, data)

        if result:
            print(result[0])
            return cls(result[0])
        else:
            return "Program not found", None
        
    @classmethod
    def update_program(cls, data):
        query = """
            UPDATE programs
            SET title = %(title)s,
                description = %(description)s
            WHERE id = %(id)s;
        """
        return connectToMySQL('workout_tracker_schema').query_db(query, data)
    
    @classmethod
    def delete_program(cls, program_id):
        query = "DELETE FROM programs WHERE id = %(id)s;"
        
        data = {
            'id' : program_id
        }

        return connectToMySQL('workout_tracker_schema').query_db(query, data)
    
    @staticmethod
    def validate_program(data):
        is_valid = True
        # Title validation
        if len(data['title']) < 2:
            flash('Title must be at least 2 characters', 'program_error')
            is_valid = False

        # Description validation
        if len(data['description']) < 2:
            flash('Description must be at least 2 characters', 'program_error')
            is_valid = False

        return is_valid
