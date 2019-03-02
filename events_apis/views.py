
from django.shortcuts import render
from events.models import Event, BookedEvent, Follow
import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.http import HttpResponse, JsonResponse, Http404

from rest_framework.generics import (
	ListAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	DestroyAPIView,
	CreateAPIView,
)

from .serializers import ( 
	EventListSerializer,
	UpcomingEventListSerializer,
	EventCreateUpdateSerializer,
	SignupSerializer,
	OrganizerEventlistSerializer,
	BookedSerializer,
	BookedCreateSerializer,
	FollowingListSerializer,
	FollowCreateSerializer,
)

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsOrganizer
from rest_framework.filters import OrderingFilter, SearchFilter



# Signup view
class SignupView(CreateAPIView):
	serializer_class = SignupSerializer
	permission_classes= [AllowAny,]



# Upcoming events list
class UpcomingEventsListView(ListAPIView):
	serializer_class = UpcomingEventListSerializer

	def get_queryset(self):
		queryset = Event.objects.all()
		queryset = queryset.filter(datetime__gte = datetime.datetime.today())
		return queryset



# List of events for a specific organizer and the users who booked it
class OrganizerEventsListView(ListAPIView):
	model = Event
	serializer_class = OrganizerEventlistSerializer
	permission_classes = [IsAuthenticated, IsOrganizer]

	def get_queryset(self):
		user = self.request.user
		return user.events.all()


# List of events that user have booked for, as a logged in user
class MyBookedEventsListView(ListAPIView):

	model = BookedEvent
	serializer_class = BookedSerializer
	permission_classes = [IsAuthenticated,]

	def get_queryset(self):
		user = self.request.user
		return user.bookedevents.all()



# To create a new event
class EventCreateView(CreateAPIView):
	serializer_class = EventCreateUpdateSerializer
	permission_classes = [IsAuthenticated,]

	def perform_create(self, serializer):
		serializer.save(organizer=self.request.user)



# To update our event
class EventUpdateView(RetrieveUpdateAPIView):
	queryset = Event.objects.all()
	serializer_class = EventCreateUpdateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
	permission_classes = [IsAuthenticated, IsOrganizer]



# To Book a ticket
class BookTicketView(CreateAPIView):
	serializer_class = BookedCreateSerializer
	permission_classes = [IsAuthenticated,]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)



# List of organizers I am following, as a logged in user
class FollowingListView(ListAPIView):
	serializer_class = FollowingListSerializer

	def get_queryset(self):
		user = self.request.user
		return user.follower.all()


class FollowView(CreateAPIView):

	serializer_class = FollowCreateSerializer
	permission_classes = [IsAuthenticated,]

	def perform_create(self, serializer):
		serializer.save(follower=self.request.user)


