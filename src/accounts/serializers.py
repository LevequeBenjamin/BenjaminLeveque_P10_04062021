"""Docstrings."""

# models
from django.utils.text import gettext_lazy as _

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import CustomUser

# rest_auth
from rest_auth.registration.serializers import RegisterSerializer

# rest_framework
from rest_framework import serializers


class CustomRegistrationSerializer(RegisterSerializer):
    """Docstrings."""
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def custom_signup(self, request, user):
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.save(update_fields=['first_name', 'last_name'])


class CustomUserSerializer(serializers.ModelSerializer):
    """Allows to serialize or deserialize the user according
     to the verb of the request."""

    class Meta:
        """Docstrings."""
        model = CustomUser
        fields = ('id', 'email', 'first_name', "last_name")


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
