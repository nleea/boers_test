from rest_framework import serializers
from src.application.auth_module.models import User
from src.application.auth_module.api.serializers.person_serializers import PersonSerializer
from django.contrib.auth.hashers import make_password
from src.interfaces.utils.auth_utils import validate_password as passwordCheck
import re

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    person = PersonSerializer(read_only=True)

class UserCreateSerializer(serializers.ModelSerializer):
    """Serializador para la creación de usuarios con Person"""

    password = serializers.CharField(write_only=True)
    person = PersonSerializer()

    class Meta:
        model = User
        fields = ["id", "username", "password", "person"]

    def validate_password(self, value):
        """Encripta la contraseña antes de guardarla"""
        return make_password(passwordCheck(value))

class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializador para la creación de usuarios con Person"""
    person = PersonSerializer(required=False)

    class Meta:
        model = User
        fields = ["id", "username", "person","active"]
        extra_kwargs = {
            'password': {'required': False}
        }
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["password"]

    def validate_password(self, value):
        return make_password(passwordCheck(value))