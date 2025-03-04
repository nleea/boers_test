from rest_framework_simplejwt.tokens import RefreshToken
from uuid import uuid4

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def generate_token():
    return str(uuid4())