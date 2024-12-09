# This file is a Python REST API that keeps track of student data
# Allows user to perform CRUD operations on the student data

# Library to build web application
from flask import Flask
# Gives access to RESTful API features
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
# Allows database integration with ORM (object-relational mapping) approach
from flask_sqlalchemy import SQLAlchemy

# Initializes Flask application instance
app = Flask(__name__)
# Implements Flask-RESTful for API
api = Api(app) 
# Configures SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# Integrates SQLAlchemy with app to allow simple interaction with databse 
db = SQLAlchemy(app)

class StudentModel(db.Model):

    """
    
    Attributes:
    ID: Integer for student's identification number
    Name: String for student's first and last name
    Degree: String for student's university degree
    Grade: Integer for student's grade for their degree
    
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    degree = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    # Transforms StudentModel object to readable format
    def __repr__(self):
        return f"Student(name = {self.name}, degree = {self.degree}, grade = {self.grade})"

# Creates database and tables based on StudentModel (run once on launch to initialize database)
with app.app_context():
    db.create_all()

# Instantiates parser to process and handle requests for creating student data
student_put_args = reqparse.RequestParser()
# Defines necessary student data to be added
student_put_args.add_argument("name", type=str, help="Name of student is required", required=True)
student_put_args.add_argument("degree", type=str, help="Degree is required", required=True)
student_put_args.add_argument("grade", type=int, help="Grade is required", required=True)

# Instantiates parser to process and handle requests for updating student data
student_update_args = reqparse.RequestParser()
# Defines optional student data to be updated
student_update_args.add_argument("name", type=str)
student_update_args.add_argument("degree", type=str)
student_update_args.add_argument("grade", type=int)

# Defines format of student data to be returned by API (in a JSON format)
resource_fields = {
    # Ensures student data formatted as integers and strings
    'id' : fields.Integer,
    'name' : fields.String,
    'degree' : fields.String,
    'grade' : fields.Integer
}

# Defines handling of requests for CRUD operations of student data
class Student(Resource):
    # Implements data formats defined in resource fields dictionary
    @marshal_with(resource_fields)
    # Handles GET request to retrieve student data using student's ID
    def get(self, student_id):
        result = StudentModel.query.filter_by(id=student_id).first() # Retrieves data from first matching student ID if found
        if not result: # If student ID does not exist, send abort error and error message
            abort(404, message="Student ID does not exist, cannot be retrieved")
        return result # Returns student data
    
    @marshal_with(resource_fields)
    # Handles PUT request to add student data using student's ID
    def put(self, student_id):
        args = student_put_args.parse_args() # Defines PUT arguments 
        result = StudentModel.query.filter_by(id=student_id).first() # Retrieves data from first matching student ID if found
        if result: # If student ID already exists, send abort error and error message
            abort(409, message="Student ID already exists, cannot be added")
        student = StudentModel(id=student_id, name = args['name'], 
        degree = args['degree'], grade = args['grade']) # Creates student object with provided student data
        db.session.add(student) # Adds new student data to the database
        db.session.commit() # Updates data with added changes in database
        return student, 201 # Returns the newly added student data

    @marshal_with(resource_fields)
    # Handles PATCH request to update student data using student's ID
    def patch(self, student_id):
        args = student_update_args.parse_args() # Defines PATCH arguments 
        result = StudentModel.query.filter_by(id=student_id).first() # Retrieves data from first matching student ID if found
        if not result: # If student ID does not exist, send abort error and error message
            abort(404, message="Student ID does not exist, cannot be updated")

        # Student data updated if new data provided as argument
        if args['name']:
            result.name = args['name']

        if args['degree']:
            result.degree = args['degree']

        if args['grade']:
            result.grade = args['grade']

        db.session.commit() # Updates data in database
        return result # Returns updated student data
        
    # Handles DELETE request to update student data using student's ID
    def delete(self, student_id):
        result = StudentModel.query.filter_by(id=student_id).first() # Retrieves data from first matching student ID if found
        if not result: # If student ID does not exist, send abort error and error message
            abort(404, message="Student does not exist, cannot be deleted")
        db.session.delete(result) # Deletes student data from the database
        db.session.commit() # Updates data in database
        return '', 204 # Return nothing (error code required)
    
# Links student resource to desired URL path
api.add_resource(Student, "/students/<int:student_id>")

# Runs Flask App in debug mode (only for testing, not for production)
if __name__ == "__main__":
    app.run(debug=True)