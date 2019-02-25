from django.contrib import admin
from .models import Location, Event, BookedEvent

admin.site.register(Location)
admin.site.register(Event)
admin.site.register(BookedEvent)