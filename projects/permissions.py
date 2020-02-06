from rest_framework import permissions
from users.models import User
from projects.models import Project


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.is_manager
        except:
            return False


class SafeOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.method in permissions.SAFE_METHODS


class IsProjectMember(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user in obj.members.all()


class IsTaskProjectMember(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user in Project.objects.get(id=view.kwargs['project_id']).members.all()


class IsTaskDeveloperOrManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.developer or request.user.is_manager
