from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer, RefreshTokenSerializer


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


class CustomUserRetrieveView(RetrieveAPIView):
    """
    Concrete view for retrieving a CustomUser instance.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # A user must be authenticated
    permission_classes = [IsAuthenticated]
