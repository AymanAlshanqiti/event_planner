
from django.urls import path
from django.conf import settings

from events_apis.views import (
	UpcomingEventsListView,
	EventUpdateView,
	# Logout,
	OrganizersEventsListView,
	EventCreateView,
	RegisterView,
	OrganizersBookedEventsListView,
)
from rest_framework_jwt.views import obtain_jwt_token #TokenObtainPairView, TokenRefreshView

urlpatterns = [

	path('api/list/', UpcomingEventsListView.as_view(), name='api-list'),
	path('api/orglist/', OrganizersEventsListView.as_view(), name='api-orglist'),
	path('api/bookedlist/', OrganizersBookedEventsListView.as_view(), name='api-bookedlist'),
	path('api/register/', RegisterView.as_view(), name='api-register'),
	path('api/create/', EventCreateView.as_view(), name='api-create'),
	path('api/<int:event_id>/update/', EventUpdateView.as_view(), name='api-update'),
	#path('api/logout/',  Logout.as_view(), name='api-logout'),
	path('api/login/', obtain_jwt_token, name= 'api-login'),
	#path('api/token/', TokenObtainPairView.as_view(), name= 'api-token'),
	#path('api/token/refresh', TokenRefreshView.as_view(), name= 'api-refresh')
]
