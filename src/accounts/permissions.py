from rest_framework.permissions import BasePermission


class IsUser(BasePermission):
    """
    Authorization at the object level to allow only the authors of an object to modify it.
    Assumes the model instance has an "author" attribute.
    """

    def has_object_permission(self, request, view, obj):
        """
        The instance must have an author attribute and be equal to the authenticated user.
        """
        if request.method == 'GET':
            return True
        return obj.email == request.user.email
