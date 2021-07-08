from rest_framework.permissions import BasePermission

from projects.models import Project, Issue


class IsAuthor(BasePermission):
    """Docstrings."""

    def has_object_permission(self, request, view, obj):
        """Docstrings."""
        return obj.author == request.user


class IsProjectAuthor(BasePermission):
    """Docstrings."""

    def has_object_permission(self, request, view, obj):
        """Docstrings."""
        project = Project.objects.get(pk=view.kwargs.get("id_projet"))
        return request.user == project.author


class IsProjectContributor(BasePermission):
    """Docstrings."""

    def has_object_permission(self, request, view, obj):
        """Docstrings."""
        project = Project.objects.get(pk=view.kwargs.get("id_projet"))
        return request.user in project.contributors


class IsContributor(BasePermission):
    """Docstrings."""

    def has_object_permission(self, request, view, obj):
        """Docstrings."""
        return obj.user == request.user
