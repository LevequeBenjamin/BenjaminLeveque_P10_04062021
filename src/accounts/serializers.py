"""Contains the serializers of accounts app."""

# django
from django.utils.text import gettext_lazy as _

# rest_framework
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers, fields

# rest_auth
from rest_auth.registration.serializers import RegisterSerializer

# models
from accounts.models import CustomUser


class CustomRegistrationSerializer(RegisterSerializer):
    """
    Inherits from RegisterSerializer.
    Allows to serialize or deserialize the register for CustomUser.
    """

    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def custom_signup(self, request, user):
        """Add firstname and lastname."""
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.save(update_fields=['first_name', 'last_name'])


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Allows to serialize or deserialize the user according
    to the verb of the request.
    """

    class Meta:
        """Meta options."""
        model = CustomUser
        fields = ('id', 'email', 'first_name', "last_name")


class RefreshTokenSerializer(serializers.Serializer):
    """
    Allows to serialize refresh token.
    """

    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def __init__(self, instance=None, data=fields.empty, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.token = None

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, attrs):
        """Set token."""
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        """
        Ensures this token is included in the outstanding token list and
        adds it to the blacklist.
        """
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class UpdatePasswordSerializer(serializers.Serializer):
    """
    Allows to serialize refresh old and new password.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class DestroyCustomUserSerializer(serializers.Serializer):
    """
    Allows to serialize password.
    """
    password = serializers.CharField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
