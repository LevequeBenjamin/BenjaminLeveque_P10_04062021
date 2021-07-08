from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer


class CustomUserListView(ListAPIView):
    """Allows to retrieve users."""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]


class CustomUserDetailView(RetrieveAPIView):
    """Allows to retrieve a user according to the id."""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
