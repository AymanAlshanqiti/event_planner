
from django.shortcuts import render
from events.models import Event, BookedEvent
import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from rest_framework.generics import (
	ListAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	DestroyAPIView,
	CreateAPIView,

)
from .serializers import (
	EventsListSerializer,
	EventCreateUpdateSerializer,
	RegisterSerializer,
	OrganizerlistSerializer,
	BookedSerializer,
)

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsOrganizer
from rest_framework.filters import OrderingFilter, SearchFilter


class UpcomingEventsListView(ListAPIView):
	serializer_class = EventsListSerializer

	def get_queryset(self):

		queryset = Event.objects.all()
		queryset = queryset.filter(datetime__gte = datetime.datetime.today())
		return queryset



# As an organizer, I can see my events and the users who booked it:
class OrganizersEventsListView(ListAPIView):
	model = Event
	serializer_class = EventsListSerializer
	permission_classes = [IsAuthenticated, IsOrganizer]

	def get_queryset(self):
		user = self.request.user
		return user.events.all()



# As an organizer or a user, I can see my booked events:
class MyBookedEventsListView(ListAPIView):

	model = BookedEvent
	serializer_class = OrganizerlistSerializer
	permission_classes = [IsAuthenticated, IsOrganizer]

	def get_queryset(self):
		user = self.request.user
		return user.bookedevents.all()



# To signup
class RegisterView(CreateAPIView):
	serializer_class = RegisterSerializer
	permission_classes= [AllowAny,]



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


