from rest_framework import serializers
from events.models import Event, BookedEvent, Location, Follow
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [ 'username']



class LocationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Location
		fields = ['city']



class BookedSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	class Meta:
		model = BookedEvent
		fields = '__all__'



class EventsListSerializer(serializers.ModelSerializer):
	location = LocationSerializer()
	organizer= UserSerializer()

	bookedevents= BookedSerializer(many=True)

	update = serializers.HyperlinkedIdentityField(
		view_name = "api-update",
		lookup_field = "id",
		lookup_url_kwarg = "event_id"
		)

	class Meta:
		model = Event
		fields = ['update', 'organizer', 'title', 'location', 'description', 'datetime', 'seats', 'bookedevents']



class OrganizerlistSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	event = EventsListSerializer()

	class Meta:
		model = BookedEvent
		fields = '__all__'



class RegisterSerializer(serializers.ModelSerializer):
	password= serializers.CharField(write_only=True)
	class Meta:
		model = User
		fields = ['username', 'password',]

	def create(self, validated_data):
		my_username = validated_data['username']
		my_password = validated_data['password']
		new_user = User(username=my_username)
		new_user.set_password(my_password)
		new_user.save()
		return validated_data



class EventCreateUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		exclude = ['organizer']





