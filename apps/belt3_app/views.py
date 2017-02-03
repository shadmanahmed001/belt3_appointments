from django.shortcuts import render, redirect
from .models import User, Appointment
from django.contrib import messages
from datetime import datetime, date

def index(request):
		return render(request,"belt3_app/main.html")

def appointments(request):
	myappt_list = Appointment.objects.filter(user_id=request.session['user_id'])

	context = {
		'appointments' : myappt_list
	}
	return render(request,"belt3_app/appointments.html", context)

def edit(request, apptid):
	context = {
		'apptid' : apptid
	}
	print apptid
	return render(request,"belt3_app/edit.html", context)

def editdone(request, apptid):
	result = Appointment.objects.editdone(apptid, request.POST)
	if result['status']:
		return redirect('/appointments')
	else:
		for errorStr in result['errors']:
			messages.error(request, errorStr)
			return render(request,"belt3_app/edit.html")

def delete(request, id):
	results= Appointment.objects.deletefunction(id)

	return redirect('/appointments')

def adder(request):
	if request.method == 'POST':
		id = request.session['user_id']
		result = Appointment.objects.adder(request.POST, id)
		if result['status']:
			return redirect ('/appointments')
		else:
			for errorStr in result['errors']:
				messages.error(request, errorStr)
			return ('/appointments')

def login(request):
	if request.method == 'POST':
		result = User.objects.login(request.POST)
		if result['status']:
			request.session['user_id'] = result['user_id']
			request.session['name'] = result['user_name']
			return redirect ('/appointments')
		else:
			for errorStr in result['errors']:
				messages.error(request, errorStr)
				return redirect ('/')

def register(request):
	if request.method == 'POST':
		result = User.objects.register(request.POST)
		if result['status']:
			request.session['user_id'] = result['user_id']
			request.session['name'] = result['name']
			return redirect ('/appointments')
		else:
			for errorStr in result['errors']:
				messages.error(request, errorStr)
	return redirect ('/')

def logout(request):
	request.session.clear()
	return redirect ('/')
