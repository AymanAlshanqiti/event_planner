from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin, EventForm
from .models import Event, BookedEvent
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
import datetime


def home(request):
	return render(request, 'home.html')


class Signup(View):
	form_class = UserSignup
	template_name = 'signup.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(user.password)
			user.save()
			messages.success(request, "You have successfully signed up.")
			login(request, user)
			return redirect("home")
		messages.warning(request, form.errors)
		return redirect("signup")


class Login(View):
	form_class = UserLogin
	template_name = 'login.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				messages.success(request, "Welcome Back!")
				return redirect('events-list')
			messages.warning(request, "Wrong email/password combination. Please try again.")
			return redirect("login")
		messages.warning(request, form.errors)
		return redirect("login")


class Logout(View):
	def get(self, request, *args, **kwargs):
		logout(request)
		messages.success(request, "You have successfully logged out.")
		return redirect("login")


def dashboard(request):
	if request.user.is_anonymous:
		messages.success(request, 'You have to signin first!')
		return redirect('login')

	events = Event.objects.filter(organizer__username__icontains = request.user.username)
	context = {
		'events': events,
	}
	return render(request, 'events/dashboard.html', context)


def events_list(request):

	if request.user.is_anonymous:
		messages.success(request, 'You have to signin first!')
		return redirect('login')

	events = Event.objects.filter(datetime__gte = datetime.datetime.today() )

	context = {
		'events': events
	}
	return render(request, 'events/list.html', context)


def event_detail(request, event_id):

	event = Event.objects.get(id=event_id)
	context = {
		"event": event,
	}
	return render(request, 'events/detail.html', context)


def event_create(request):
	if request.user.is_anonymous:
		return redirect('login')

	form = EventForm()

	if request.method == "POST":
		form = EventForm(request.POST)
		if form.is_valid():
			event = form.save(commit=False)
			event.organizer = request.user
			event.save()
			return redirect('events-list')
	context = {
		"form":form,
	}
	return render(request, 'events/create.html', context)


def event_update(request, event_id):
	event = Event.objects.get(id=event_id)

	if not(request.user == event.organizer):
		messages.success(request, "you can't update this event")
		return redirect("events-list")

	form = EventForm(instance=event)


	if request.method == "POST":
		form = EventForm(request.POST, instance=event)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Edited!")
			return redirect('events-list')
		print (form.errors)

	context = {
	"form": form,
	"event": event,
	}
	return render(request, 'events/update.html', context)
