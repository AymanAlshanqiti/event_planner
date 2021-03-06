from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin, EventForm, UserEditForm
from .models import Event, BookedEvent, Follow
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q 
import datetime
from django.utils import timezone

from django.core.mail import send_mail
from django.conf import settings


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

	# events = Event.objects.filter(organizer__username__icontains = request.user.username)
	events = request.user.events.all()
	context = {
		'events': events,
	}
	return render(request, 'users/dashboard.html', context)



def user_profile(request, organizer_id):
	if request.user.is_anonymous:
		messages.success(request, 'You have to signin first!')
		return redirect('login')

	organizer_obj = User.objects.get(id=organizer_id)
	followers = organizer_obj.follower.all().values_list('follower__id', flat=True)
	following = organizer_obj.following.all().values_list('follower__id', flat=True)

	events = organizer_obj.events.all()
	context = {
		'events': events,
		'organizer_obj': organizer_obj,
		'followers': followers,
		'following': following,
	}
	return render(request, 'users/profile.html', context)



def edit_profile(request):
	if request.user.is_anonymous:
		messages.success(request, 'You have to signin first!')
		return redirect('login')

	form = UserEditForm(instance=request.user)

	if request.method == "POST":
		form = UserEditForm(request.POST, instance=request.user)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(user.password)
			user.save()
			messages.success(request, "You have successfully updated your profile.")
			login(request, user)
			return redirect("user-profile", request.user.id)

		messages.warning(request, form.errors)
		return redirect("user-profile", request.user.id)

	context = {
	"form": form,
	}
	return render(request, 'users/edit.html', context)



def user_booked_events(request):
	if request.user.is_anonymous:
		messages.success(request, 'You have to signin first!')
		return redirect('login')

	booked_events = BookedEvent.objects.filter(user__username__icontains = request.user.username)

	context = {
		'booked_events': booked_events
	}
	return render(request, 'booked_events/user_booked_events.html', context)



def cancel_booked_events(request, ticket_id): 
	if request.user.is_anonymous:
		messages.success(request, 'You have to signin first!')
		return redirect('login')

	user_ticket = BookedEvent.objects.get(id= ticket_id).delete()
	return redirect('user-booked-events')



def follow(request, user_id):
	if request.user.is_anonymous:
		messages.success(request, 'You have to signin first!')
		return redirect('login')

	user_following = User.objects.get(id=user_id)
	follow, created = Follow.objects.get_or_create(follower=request.user, following=user_following)

	if created:
		following = True
	else:
		following = False
		follow.delete()

	following_count = user_following.following.all().count()
	print(following_count)

	respose = {
		"following": following,
		"following_count": following_count,
	}
	return JsonResponse(respose, safe=False)




def events_list(request):

	if request.user.is_anonymous:
		messages.success(request, 'You have to signin first!')
		return redirect('login')

	events = Event.objects.filter(datetime__gte = datetime.datetime.today() )
	query = request.GET.get("search")

	if query:
		events = events.filter(
			Q(title__icontains = query)|
			Q(description__icontains = query)|
			Q(organizer__username__icontains = query)
			).distinct()

	context = {
		'events': events
	}
	return render(request, 'events/list.html', context)



def event_detail(request, event_id):

	event = Event.objects.get(id=event_id)
	tickets = event.bookedevents.all()

	event_seats = event.seats
	ticket_count = 0

	for buyer in tickets:
		ticket_count += buyer.ticket

	tickets_left = event_seats - ticket_count

	context = {
		"event": event,
		"tickets": tickets,
		"tickets_left": tickets_left,
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

			following = request.user.following.all().values_list('follower__email', flat=True)
			subject = 'New Event Aleeert'
			message = "Check out my new event: %s " %(event.title)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = []
			for user in following:
				recipient_list.append(user)

			send_mail( subject, message, email_from, recipient_list )
			
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



def booked_event(request):
	if request.user.is_anonymous:
		return redirect('login')

	event_id = request.POST.get("event_id")
	user_ticket_num = request.POST.get("ticket_num")
	event = Event.objects.get(id=event_id)

	tickets = event.bookedevents.all()
	event_seats = event.seats
	ticket_count = 0

	for buyer in tickets:
		ticket_count += buyer.ticket

	tickets_left = event_seats - ticket_count

	if user_ticket_num != "":

		if int(user_ticket_num) > event.tickets_left():
			messages.warning(request, 'sorry, not enough tickets left')
			return redirect('event-detail', event_id)

		elif  int(user_ticket_num) == 0:
			messages.warning(request, 'enter valid number')
			return redirect('event-detail', event_id)

		else:
			ticket = BookedEvent()
			ticket.user = request.user
			ticket.event = event
			ticket.ticket = user_ticket_num
			ticket.save()

			subject = 'Thank you for buying a ticket'
			message = " You've successfuly booked %s tickets for %s event " %(ticket.ticket, ticket.event.title)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [ticket.user.email]
			send_mail( subject, message, email_from, recipient_list )
			return redirect('event-detail', event_id)

	else:
		messages.warning(request, "Please Enter a valid ticket number")

	context = {
		"event" : event,
		"tickets_left": tickets_left,
		"tickets": tickets,
	}
	return render(request, 'events/detail.html', context)




def email(request, ):
   subject = 'Thank you for registering to our site'
   message = ' it  means a world to us '
   email_from = settings.EMAIL_HOST_USER
   recipient_list = ['ayman.alshanqiti@gmail.com','nujoodalmadi@gmail.com']
   send_mail( subject, message, email_from, recipient_list )
   return redirect('events-list')


