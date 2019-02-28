from django.urls import path
from .views import Login, Logout, Signup
from events import views

urlpatterns = [
	path('', views.home, name='home'),

	############ Auth urls ############ 

    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),


    ############ User urls ############

	path('dashboard/', views.dashboard, name='dashboard'),
	path('user/<int:user_id>/profile', views.user_profile, name='user-profile'),
	path('profile/edit/', views.edit_profile, name="edit-profile"),
	path('user/bookedevents', views.user_booked_events, name='user-booked-events'),
	path('follow/<int:user_id>/', views.follow, name='follow'),
	path('ticket/<int:ticket_id>/cancel/', views.cancel_booked_events, name='cancel-ticket'),


	############ Event urls ############

    path('events/list/', views.events_list, name='events-list'),
	path('event/create/',views.event_create ,name='event-create'),
	path('event/<int:event_id>/',views.event_detail ,name='event-detail'),
    path('event/<int:event_id>/update/', views.event_update, name='event-update'),
	path('booked/', views.booked_event, name='booked'),
]
