""" 
	Sample Model File

	A Model should be in charge of communicating with the Database. 
	Define specific model method that query the database for information.
	Then call upon these model method in your controller.

	Create a model using this template.
"""
from system.core.model import Model
import re
class User(Model):
	def __init__(self):
		super(User, self).__init__()

	def get_user_by_email(self, email_address):
		# pass data to the query like so
		query = "SELECT first_name, email_address, password FROM users WHERE email_address = :email_address"
		data = { 
			'email_address': email_address
		}
		return self.db.query_db(query, data)[0]

	def add_user(self, user):
		# We write our validations in model functions.
		# They will look similar to those we wrote in Flask
		email_regex = re.compile(r"^[^@]+@[^@]+\.[^@]+$")
		errors = []
		# Some basic validation
		if not user['first_name']:
			errors.append('First name cannot be blank')
		elif not user['last_name']:
			errors.append('Last name cannot be blank')
		elif len(user['first_name']) < 2 or len(user['last_name']) < 2:
			errors.append('Name must be at least 2 characters long')
		if not user['email_address']:
			errors.append('Email cannot be blank')
		elif not email_regex.match(user['email_address']):
			errors.append('Email format is not valid!')
		if not user['password']:
			errors.append('Password cannot be blank')
		elif len(user['password']) < 8:
			errors.append('Password must be at least 8 characters long')
		elif user['password'] != user['c_password']:
			errors.append('Password and confirmation do not match')
		# If we hit errors, return them, else return True.
		if errors:
			return {"status": False, "errors": errors}
		else:
			password_hash = self.bcrypt.generate_password_hash(user['password'])
			# Build the query first and then the data that goes in the query
			query = "INSERT INTO users (first_name, last_name, email_address, password, created_at) VALUES (:first_name, :last_name, :email_address, :password, NOW())"
			data = { 
				'first_name': user['first_name'],
				'last_name': user['last_name'], 
				'email_address': user['email_address'],
				'password': password_hash 
			}
			self.db.query_db(query, data)
			return { "status": True }

	# def update_course(self, course):
	#   	# Building the query for the update
	#   	query = "UPDATE courses SET title=:title, description=:description WHERE id = :course_id"
	#   	# we need to pass the necessary data
	#   	data = { 'title': course['title'], 'description': course['description'], 'course_id': course['id']}
	#   	# run the update
	#   	return self.db.query_db(query, data)

	# def delete_course(self, course_id):
	#   	query = "DELETE FROM courses WHERE id = :course_id"
	#   	data = { "course_id": course_id }
	#   	return self.db.query_db(query, data)