from rest_framework import serializers
from events.models import Event, BookedEvent, Location, Follow
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username']



class LocationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Location
		fields = ['id', 'city'] 



class EventListSerializer(serializers.ModelSerializer):
	organizer = UserSerializer()
	location = LocationSerializer()

	class Meta:
		model = Event
		fields = '__all__'
		


class BookedSerializer(serializers.ModelSerializer):
	event = EventListSerializer()

	class Meta:
		model = BookedEvent
		fields = ['user', 'event', 'ticket']



class AttendantEventSerializer(serializers.ModelSerializer):
	user = UserSerializer()

	class Meta:
		model = BookedEvent
		fields = ['user', 'ticket']



class UpcomingEventListSerializer(serializers.ModelSerializer):
	location = LocationSerializer()
	organizer = UserSerializer()

	class Meta:
		model = Event
		fields = ['id', 'title', 'organizer', 'location', 'description', 'datetime', 'seats']



class OrganizerEventlistSerializer(serializers.ModelSerializer):
	bookedevents = AttendantEventSerializer(many=True)

	# A link that take us to update API URL
	update = serializers.HyperlinkedIdentityField(
		view_name = "api-event-update",
		lookup_field = "id",
		lookup_url_kwarg = "event_id"
	)

	class Meta:
		model = Event
		fields = ['id', 'title', 'organizer', 'location', 'description', 'datetime', 'seats', 'update', 'bookedevents']



class SignupSerializer(serializers.ModelSerializer):

	""" We overrode the password field and set the write_only attribute to True
		so that it won't be displayed in the response """
	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password',]

	# We adjust the "create method" to hash the user's password
	def create(self, validated_data):
		my_username = validated_data['username']
		my_first_name = validated_data['first_name']
		my_last_name = validated_data['last_name']
		my_email = validated_data['email']
		my_password = validated_data['password']
		new_user = User(username=my_username)
		new_user.set_password(my_password)
		new_user.save()
		return validated_data



class EventCreateUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		exclude = ['organizer']



class BookedCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = BookedEvent
		exclude = ['user']


# List of the users who I followed
class FollowingListSerializer(serializers.ModelSerializer):
	following = UserSerializer()

	class Meta:
		model = Follow
		fields = ['following']
		
		
# Follow some one
class FollowCreateSerializer(serializers.ModelSerializer):
	following = UserSerializer()

	class Meta:
		model = Follow
		exclude = ['follower']
		





