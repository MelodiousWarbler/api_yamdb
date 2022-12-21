from rest_framework import permissions

from reviews.models import ADMIN


class isAdminOrOnlyRead(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role is ADMIN
            or request.method in permissions.SAFE_METHODS
        )
