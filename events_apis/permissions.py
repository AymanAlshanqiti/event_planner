from rest_framework.permissions import BasePermission

class IsOrganizer(BasePermission):
    message = "Only the organizer of this event/s can make this action "

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or obj.organizer == request.user:
            return True
        return False
