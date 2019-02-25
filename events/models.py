from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse





class Location(models.Model):
	city =  models.CharField(max_length=120)

	def __str__(self):
		return self.city


class Event(models.Model):
	organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "events")
	title = models.CharField(max_length=120)
	location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name= "locations")
	description = models.TextField()
	datetime = models.DateTimeField()
	seats = models.PositiveIntegerField()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('event-detail' , args= [str(self.id)])


class BookedEvent(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "bookedevents")
	event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name= "bookedevents")



