"""Contains the permissions of accounts app."""

# rest_framework
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission

from accounts.models import CustomUser


class IsUser(BasePermission):
    """
    Authorization at the object level to allow only the authors of an object to modify it.
    Assumes the model instance has an "author" attribute.
    Return true if it's a get method and the user is admin.
    """

    def has_object_permission(self, request, view, obj):
        """
        The instance must have an author attribute and be equal to the authenticated user.
        """
        if request.method == 'GET':
            return True
        if request.user.is_superuser:
            return True
        return obj.email == request.user.email


class IsUserRequest(BasePermission):
    """
    Authorization at the object level to allow only the authors of an object to modify it.
    Assumes the model instance has an "author" attribute.
    Return true if it's a get method and the user is admin.
    """

    def has_permission(self, request, view):
        """
        The instance must have an author attribute and be equal to the authenticated user.
        """
        obj = get_object_or_404(CustomUser, pk=view.kwargs.get("pk"))
        if request.method == 'GET':
            return True
        if request.user.is_superuser and request.method == 'DELETE':
            return True
        return obj.email == request.user.email
