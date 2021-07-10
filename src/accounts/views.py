from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, get_object_or_404, \
    RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import CustomUser
from accounts.permissions import IsUser
from accounts.serializers import CustomUserSerializer, RefreshTokenSerializer, UpdatePasswordSerializer, \
    DestroyCustomUserSerializer


class CustomUserListView(ListAPIView):
    """
    Concrete view for listing a queryset or creating a Project instance.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # A user must be authenticated
    permission_classes = [IsAuthenticated]


class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    # A user must be authenticated
    permission_classes = [IsAuthenticated]

    def post(self, request, *args):
        """Docstrings."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomUserRetrieveView(RetrieveUpdateAPIView):
    """
    Concrete view for retrieving a CustomUser instance.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # A user must be authenticated
    permission_classes = [IsAuthenticated, IsUser]


class CustomUserDestroyView(DestroyAPIView):
    """
    Concrete view for retrieving a CustomUser instance.
    """

    queryset = CustomUser.objects.all()
    serializer_class = DestroyCustomUserSerializer
    # A user must be authenticated
    permission_classes = [IsAuthenticated, IsUser]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.check_password(request.data.get("password")):
            raise ValidationError("The password does not match.")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomUserUpdatePasswordView(UpdateAPIView):
    """
    Concrete view for retrieving a CustomUser instance.
    """

    queryset = CustomUser.objects.all()
    serializer_class = UpdatePasswordSerializer
    # A user must be authenticated
    permission_classes = [IsAuthenticated, IsUser]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not instance.check_password(serializer.data.get("old_password")):
            raise ValidationError("The password does not match.")
        instance.set_password(serializer.data.get("new_password"))
        self.perform_update(instance)
        return Response({"Password updated successfully"}, status=status.HTTP_200_OK)
