# views.py

from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from src.interfaces.utils.auth_utils import get_tokens_for_user
from src.application.auth_module.api.validators.auth_validator import AuthValidator
from src.application.auth_module.api.repositories.factory_repository import (
    AuthModuleRepositoryFactory,
)
from src.application.auth_module.api.serializers.auth_serializer import SchemaResponseLogin, SchemaRequestForgetPassword, SchemaRequestChangePassword
from drf_spectacular.utils import extend_schema
from src.application.auth_module.api.serializers.user_serializers import UserSerializer, ChangePasswordSerializer
from src.interfaces.utils.email_utils import send_forget_password_mail
from src.interfaces.utils.auth_utils import generate_token


class AuthView(ViewSet):
    factory = None

    def get_serializer_class(self):
        if self.action == 'change_password':
            return ChangePasswordSerializer
        return UserSerializer
    
    @property
    def get_service(self):
        if not self.factory:
            self.factory = AuthModuleRepositoryFactory.get_user_service(self.get_serializer_class())
        return self.factory
    
    @extend_schema(
        responses={200: SchemaResponseLogin},
    )
    @action(detail=False, methods=["POST"])
    def login(self, request):

        validator = AuthValidator(data=request.data)

        if validator.is_valid():
            token = get_tokens_for_user(validator.validated_data)
            return Response({ "token" :{ **token } }, status=status.HTTP_200_OK)
        return Response({"Invalid credentias"}, status=status.HTTP_401_UNAUTHORIZED)

    @extend_schema(
        request=SchemaRequestForgetPassword,
    )
    @action(detail=False, methods=["POST"])
    def forget_password(self, request):
        email = request.data.get("email")
        
        if not email:
            return Response({"email": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        
        instance = self.get_service.get_by_email(email)
        
        if not instance:
            return Response({"email": ["User not found"]}, status=status.HTTP_404_NOT_FOUND)
        
        token = generate_token()
        self.get_service.update(instance.id, {"token": token})
        send_forget_password_mail(instance.email, token)
        
        return Response({"message": "Email sent"}, status=status.HTTP_200_OK)
    
    @extend_schema(
        request=SchemaRequestChangePassword,
    )
    @action(detail=False, methods=["POST"])
    def change_password(self, request):
        new_password = request.data.get("new_password")
        token = request.data.get("token")
        
        if not new_password or not token:
            return Response({"message": "there is a error, check the data"}, status=status.HTTP_400_BAD_REQUEST)
        
        instance = self.get_service.get_by_token(token)
        serializer = self.get_serializer_class()(instance, data={"password": new_password})
        
        if serializer.is_valid():
            self.get_service.update(instance.id, serializer.validated_data)
            return Response({"message": "Password updated"}, status=status.HTTP_200_OK)
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        