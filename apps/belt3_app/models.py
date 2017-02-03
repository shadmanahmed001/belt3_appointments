from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
	def login(self, post):
		email = post['email'].lower().strip()
		password = post['password']

		errors =[]
		if len(email) == 0:
			errors.append('email is required')
		elif not User.objects.filter(email = email).exists():
			errors.append('email is not in the database')

		if not errors:
			user_list = User.objects.filter(email = email)
			user = user_list[0]
			password = password.encode()
			ps_hashed = user.password.encode()
			if bcrypt.hashpw(password, ps_hashed) == ps_hashed:
				return {'status': True, 'user_id': user.id, 'user_name' : user.name}
			else:
				errors.append('email or password does not match')
		return {'status': False, 'errors': errors}

	def register(self, post):
		email = post['email'].lower().strip()
		name = post['name']
		last = post['last']
		password = post['password']
		confirm_password = post['confirm_password']

		errors = []
		if not EMAIL_REGEX.match(email):
			errors.append(' Invalid email ')
		if not NAME_REGEX.match(name):
			errors.append(' Invalid name ')
		if not NAME_REGEX.match(last):
			errors.append(' Invalid last ')
		if len(password) < 8:
			errors.append(' Password must be atleast 8 characters long ')
		elif password != confirm_password:
			errors.append(' Password and confirm password are not matched ')

		if not errors:
			already_user_list = User.objects.filter(email=email)
			if not already_user_list:
				password = password.encode()
				hashed = bcrypt.hashpw(password, bcrypt.gensalt())
				print "this means new user"
				user = User.objects.create(name=name,last=last,email = email,password=hashed,)
				print ('**************')
				return {'status': True, 'user_id': user.id, 'name' : name}
			else:
				errors.append('Please login below. Your email already exists in our DB')
				print 'this means its a returning user but logging in the wrong place'

		return {'status': False, 'errors': errors}

	def adder(self, post, id):
		task = post['task']
		status = post['status']
		date = post['date']
		time = post['time']
		errors =[]
		if len(task) and len(status) and len (date) and len (time) == 0:
			errors.append('You left blank fields')
			return {
			'status': False,
			'errors': errors
			}
		userlist = User.objects.filter(id=id)
		userlist[0]
		Appointment.objects.create(task=task, status=status, date=date, time=time, user=userlist[0])
		return {
		'status' : True
		}

	def editdone(request, apptid, post):
		task = post['task']
		status = post['status']
		date = post['date']
		time = post['time']
		results = Appointment.objects.filter(id=apptid).update(task=task, status=status, date=date, time=time)
		errors = []
		if not results:
			errors.append('something went wrong here buddy')
			return {
			'status': False,
			'errors': errors
			}
		else:
			return {
			'status' : True

			}

	def deletefunction(request, id):
		Appointment.objects.filter(id=id).delete()
		return True

class User(models.Model):
	name = models.CharField(max_length=45)
	last = models.CharField(max_length=45)
	email = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

class Appointment(models.Model):
	task = models.CharField(max_length=45)
	status = models.CharField(max_length=45, default='pending')
	date = models.DateTimeField(blank=True)
	time = models.TimeField(blank=True)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	user = models.ForeignKey(User)
	objects = UserManager()
