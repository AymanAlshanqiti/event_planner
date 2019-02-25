from django.urls import path
from .views import Login, Logout, Signup
from events import views

urlpatterns = [
	path('', views.home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('events/list/', views.events_list, name='events-list'),
]