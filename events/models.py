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
	pic = models.ImageField(null=True, blank=True)
	location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name= "locations")
	description = models.TextField()
	datetime = models.DateTimeField()
	seats = models.PositiveIntegerField()

	def __str__(self):
		return "%s --- %s --- %s" % (self.title, self.organizer.username, self.datetime)

	def get_absolute_url(self):
		return reverse('event-detail' , args= [str(self.id)])

	def tickets_left(self):
		return self.seats - sum(self.bookedevents.all().values_list('ticket', flat=True))



class BookedEvent(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "bookedevents")
	event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name= "bookedevents")
	ticket = models.PositiveIntegerField()

	def __str__(self):
		return "id = %s --- %s --- %s --- %s" % (self.id, self.user.username, self.event.title, self.ticket)



class Follow(models.Model):
	# User who follow other user
	follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "follower")

	# User who's following by other user
	following = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "following")













		
