
from django.shortcuts import render
from events.models import Event
import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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
	OrgBookedEventsList,

)

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsOrganizer
from rest_framework.filters import OrderingFilter, SearchFilter





class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UpcomingEventsListView(ListAPIView):
	serializer_class = EventsListSerializer

	def get_queryset(self):

		queryset = Event.objects.all()
		queryset = queryset.filter(datetime__gte = datetime.datetime.today())
		return queryset


class OrganizersEventsListView(ListAPIView):
	model = Event
	serializer_class = EventsListSerializer
	permission_classes = [IsAuthenticated, IsOrganizer]

	def get_queryset(self):
		user = self.request.user
		return user.events.all()

#as organizer, I can see who booked "my" events:
class OrganizersBookedEventsListView(ListAPIView):

	model = Event
	serializer_class = OrgBookedEventsList
	permission_classes = [IsAuthenticated, IsOrganizer]

	def get_queryset(self):
		user = self.request.user
		return user.events.all()


class RegisterView(CreateAPIView):
	serializer_class = RegisterSerializer
	permission_classes= [AllowAny,]


class EventCreateView(CreateAPIView):
	serializer_class = EventCreateUpdateSerializer
	permission_classes = [IsAuthenticated,]

	def perform_create(self, serializer):
		serializer.save(organizer=self.request.user)


class EventUpdateView(RetrieveUpdateAPIView):
	queryset = Event.objects.all()
	serializer_class = EventCreateUpdateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
	permission_classes = [IsAuthenticated, IsOrganizer]

#as a user, I can see (a list) the events I booked:
