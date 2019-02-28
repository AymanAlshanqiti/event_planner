
from django.urls import path
from django.conf import settings

from events_apis.views import (
	UpcomingEventsListView,
	EventUpdateView,
	OrganizerEventsListView,
	EventCreateView,
	SignupView,
	MyBookedEventsListView,
	BookTicketView,
	FollowingListView,
)

from rest_framework_jwt.views import obtain_jwt_token 

urlpatterns = [

	path('api/events/list/', UpcomingEventsListView.as_view(), name='api-event-list'),
	path('api/org-events/', OrganizerEventsListView.as_view(), name='api-orglist'),
	path('api/my-booked-list/', MyBookedEventsListView.as_view(), name='api-my-booked-list'),
	path('api/signup/', SignupView.as_view(), name='api-signup'),
	path('api/event/create/', EventCreateView.as_view(), name='api-event-create'),
	path('api/event/<int:event_id>/update/', EventUpdateView.as_view(), name='api-event-update'),

	path('api/booked/create/', BookTicketView.as_view(), name='api-book-create'),
	path('api/following/', FollowingListView.as_view(), name='api-following'),

	# Login using JWT library that comming from django rest framework
	path('api/login/', obtain_jwt_token, name= 'api-login'),
]
