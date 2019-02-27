from rest_framework import serializers
from events.models import Event, BookedEvent, Location, Follow
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [ 'username']

#this does not work
# class UserLoginSerializer(serializers.Serializer):
# 	token = serializers.CharField(allow_blank=True, read_only=True)

# 	def validate(self, data):

# 		jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
# 		jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# 		payload = jwt_payload_handler(user_obj)
# 		token = jwt_encode_handler(payload)

# 		data["token"] = token
# 		return data


class LocationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Location
		fields = ['city']


class EventsListSerializer(serializers.ModelSerializer):
	location = LocationSerializer()
	organizer= UserSerializer()


	update = serializers.HyperlinkedIdentityField(
		view_name = "api-update",
		lookup_field = "id",
		lookup_url_kwarg = "event_id"
		)


	class Meta:
		model = Event
		fields = ['update', 'organizer', 'title', 'location', 'description', 'datetime', 'seats']



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



class BookedSerializer(serializers.ModelSerializer):
	user = UserSerializer()

	class Meta:
		model = BookedEvent
		fields = ['user']


# as an organizer, I can see who (user) booked for my event
class OrgBookedEventsList(serializers.ModelSerializer):
	bookedevents= BookedSerializer(many=True)

	booked_count= serializers.SerializerMethodField()

	class Meta:
		model = Event
		fields = ['title', 'booked_count', 'bookedevents']

	def get_booked_count(self, obj):
		return obj.bookedevents.count()
