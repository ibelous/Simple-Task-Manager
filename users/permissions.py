from rest_framework import permissions
from .models import User


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.is_manager
        except:
            return False


class IsOwnerOrManager(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id or obj.user_type == 'Developer'
