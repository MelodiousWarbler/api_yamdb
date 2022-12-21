from rest_framework import permissions

from reviews.models import ADMIN


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_admin
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_admin
            or request.user.is_staff
        )


class isAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role is ADMIN
            or request.method in permissions.SAFE_METHODS
        )
