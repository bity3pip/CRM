from rest_framework.permissions import BasePermission


class IsChatter(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_chatter


class IsChatterOrTeamlead(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_chatter or request.user.is_teamlead
        )
