from rest_framework_simplejwt.tokens import RefreshToken
from uuid import uuid4
import re
from rest_framework import serializers

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def generate_token():
    return str(uuid4())


def validate_password(value):
    errors = []

    if not any(c.islower() for c in value):
        errors.append("La contraseña debe contener al menos una letra minúscula.")
        
    if not any(c.isupper() for c in value):
        errors.append("La contraseña debe contener al menos una letra mayúscula.")
        
    if not any(c.isdigit() for c in value):
        errors.append("La contraseña debe contener al menos un número.")
        
    if len(value) < 8:
            errors.append("La contraseña debe tener al menos 8 caracteres.")
            
    if not re.search(r'[@$!%*?&]', value):
            errors.append("La contraseña debe incluir un carácter especial (@$!%*?&).")

    if errors:
        raise serializers.ValidationError(errors)

    return value 