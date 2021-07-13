"""Contains the views of accounts app."""

# rest_framework
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, UpdateAPIView, \
    RetrieveUpdateAPIView, DestroyAPIView, get_object_or_404, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# models
from accounts.models import CustomUser

# permissions
from accounts.permissions import IsUser, IsUserRequest

# serializers
from accounts.serializers import CustomUserSerializer, RefreshTokenSerializer, \
    UpdatePasswordSerializer, DestroyCustomUserSerializer


class CustomUserListView(ListAPIView):
    """
    Concrete view for listing a queryset or creating a CustomUser instance.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # A user must be authenticated.
    permission_classes = [IsAuthenticated]


class LogoutView(GenericAPIView):
    """
    Concrete view for adds the token to the blacklist.
    """
    serializer_class = RefreshTokenSerializer
    # A user must be authenticated, be the user.
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Docstrings."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomUserRetrieveUpdateView(RetrieveUpdateAPIView):
    """
    Concrete view for retrieving, updating a CustomUser instance.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # A user must be authenticated, be the user or admin.
    permission_classes = [IsAuthenticated, IsUser]


class CustomUserDestroyView(DestroyAPIView):
    """
    Concrete view for deleting a CustomUser instance.
    """

    queryset = CustomUser.objects.all()
    serializer_class = DestroyCustomUserSerializer
    # A user must be authenticated, be the user.
    permission_classes = [IsAuthenticated, IsUserRequest]

    def get_object(self):
        """Returns the object the view is displaying."""
        obj = self.request.user
        return obj

    def destroy(self, request, *args, **kwargs):
        """Destroy a CustomUser instance."""
        instance = self.get_object()
        # confirm password
        if not instance.check_password(request.data.get("password")):
            raise ValidationError("The password does not match.")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomUserUpdatePasswordView(UpdateAPIView):
    """
    Concrete view for updating a password of CustomUser instance.
    """

    queryset = CustomUser.objects.all()
    serializer_class = UpdatePasswordSerializer
    # A user must be authenticated and be the user.
    permission_classes = [IsAuthenticated, IsUserRequest]

    def get_object(self):
        """Returns the object the view is displaying."""
        obj = get_object_or_404(CustomUser, pk=self.kwargs.get("pk"))
        return obj

    def update(self, request, *args, **kwargs):
        """Update a CustomUser instance."""
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # confirm password
        if not instance.check_password(serializer.data.get("old_password")):
            raise ValidationError("The password does not match.")
        instance.set_password(serializer.data.get("new_password"))
        self.perform_update(instance)
        return Response({"Password updated successfully"}, status=status.HTTP_200_OK)
