"""Contains the permissions of projects app."""

# rest_framework
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission

# models
from projects.models import Project


class IsAuthor(BasePermission):
    """
    Verification of global authorizations for project authors.
    Return true if it's a get method and the user is admin.
    """

    def has_object_permission(self, request, view, obj):
        """
        The instance must have an author attribute and be equal to the authenticated user.
        """
        if request.method == 'GET' and request.user in obj.contributors.all():
            return True
        if request.user.is_superuser:
            return True
        return request.user == obj.author


class IsAuthorOrContributor(BasePermission):
    """
    Authorization at the object level to allow only the authors of an object to modify it.
    Assumes the model instance has an "author" attribute.
    Return true if it's a get method and the user is admin.
    """

    def has_object_permission(self, request, view, obj):
        """
        The instance must have an author attribute and be equal to the authenticated user.
        """
        project = get_object_or_404(Project, pk=view.kwargs.get("id_project"))
        if request.method == 'GET' and request.user in project.contributors.all():
            return True
        if request.user.is_superuser:
            return True
        return obj.author == request.user


class IsProjectAuthor(BasePermission):
    """
    Verification of global authorizations for project authors.
    Return true if it's a get method and the user is admin.
    """

    def has_permission(self, request, view):
        """
        The instance must have an author attribute and be equal to the authenticated user.
        """
        project = get_object_or_404(Project, pk=view.kwargs.get("id_project"))
        if request.method == 'GET' and request.user in project.contributors.all():
            return True
        if request.user.is_superuser:
            return True
        return request.user == project.author


class IsProjectContributor(BasePermission):
    """
    Verification of global authorizations for project contributors.
    """

    def has_permission(self, request, view):
        """
        The instance must have an author attribute and must contain the authenticated user.
        """
        project = get_object_or_404(Project, pk=view.kwargs.get("id_project"))
        if project.author == request.user:
            return True
        return request.user in project.contributors.all()
