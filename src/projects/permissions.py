from rest_framework.permissions import BasePermission

from projects.models import Project, Issue


class IsAuthor(BasePermission):
    """
    Authorization at the object level to allow only the authors of an object to modify it.
    Assumes the model instance has an "author" attribute.
    """

    def has_object_permission(self, request, view, obj):
        """
        The instance must have an author attribute and be equal to the authenticated user.
        """
        return obj.author == request.user


class IsProjectAuthor(BasePermission):
    """
    Verification of global authorizations for project authors.
    """

    def has_permission(self, request, view):
        """
        The instance must have an author attribute and be equal to the authenticated user.
        """
        project = Project.objects.get(pk=view.kwargs.get("id_project"))
        return request.user == project.author


class IsProjectContributor(BasePermission):
    """
    Verification of global authorizations for project contributors.
    """

    def has_permission(self, request, view):
        """
        The instance must have an author attribute and must contain the authenticated user.
        """
        project = Project.objects.get(pk=view.kwargs.get("id_project"))
        return request.user in project.contributors.all()


class IsContributor(BasePermission):
    """
    Authorization at the object level to allow only the authors of an object to modify it.
    Assumes the model instance has an "user" attribute.
    """

    def has_object_permission(self, request, view, obj):
        """
        The instance must have an user attribute and be equal to the authenticated user.
        """
        return obj.user == request.user
