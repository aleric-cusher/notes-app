from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user == obj
        return False
        