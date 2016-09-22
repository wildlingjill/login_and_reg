from system.core.controller import *
class Users(Controller):
	def __init__(self, action):
		super(Users, self).__init__(action)
		# Note that we have to load the model before using it
		self.load_model('User')

	def index(self):
		# course_id = self.db.query_db('SELECT id from courses')
		return self.load_view('index.html')

	# This is how a method with a route parameter that provides the id would work
	# We would set up a GET route for this method
	def login(self):
		email_address = request.form['email_address']
		password = request.form['password']
		user = self.models['User'].get_user_by_email(email_address)
		if not self.models['User'].bcrypt.check_password_hash(user['password'], password):
			flash('Information given does not match login credentials!')
			return redirect('/')
		else:
			session['email'] = email_address
			session['success'] = 'logged in'
			return redirect('/success')

	# This is how a method used to add a course would look
	# We would set up a POST route for this method
	def register(self):
		user_info = {
			"first_name" : request.form['first_name'],
			"last_name" : request.form['last_name'],
			"email_address" : request.form['email_address'],
			"password" : request.form['password'],
			"c_password" : request.form['c_password']
		}
		validations = self.models['User'].add_user(user_info)
		if validations['status'] == False:
			for message in validations['errors']:
				flash(message, 'error')
				return redirect('/')
		else:
			session["email"] = request.form['email_address']
			session['success'] = 'registered'	
			return redirect('/success')


	def success(self):
		user = self.models['User'].get_user_by_email(session["email"])
		session['name'] = user['first_name']
		return self.load_view('success.html', name=session['name'], success_message = session['success'])


	def logout(self):
		flash('You are now logged out')
		return redirect('/')

	# This is how a method used to update a course would look
	# We would set up a POST route for this method
	# def update(self, course_id):
	# 	# in actuality, data for updating the course would come 
	# 	# from a form on our client
	# 	course_details = {
	# 		'id': course_id,
	# 		'title': 'Python 2.0',
	# 		'description': 'This course is unreal!'
	# 	}
	# 	self.models['Course'].update_course(course_details)
	# 	return redirect('/')

	 # This is how a method used to delete a course would look
	 # We would set up a POST route for this method

	# def destroy(self, course_id):
	# 	course = self.models['Course'].get_course_by_id(course_id)
	# 	print course
	# 	return self.load_view('delete.html', course=course)

	# def delete(self, course_id):
	# 	self.models['Course'].delete_course(course_id)
	# 	return redirect('/')




