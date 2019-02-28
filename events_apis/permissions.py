from rest_framework.permissions import BasePermission

class IsOrganizer(BasePermission):
    message = "Only the organizer of this event/s can access"

    """ We've overwrite this method from BasePermission class
    	to let it decide whether the user will be permitted access or not """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or (obj.organizer == request.user):

        	# That's mean user has access
            return True

        # That's mean user doesn't has access
        return False
