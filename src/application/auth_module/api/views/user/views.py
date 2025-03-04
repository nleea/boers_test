# views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from src.application.auth_module.api.repositories.factory_repository import (
    AuthModuleRepositoryFactory,
)
from src.application.auth_module.api.serializers.user_serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer
)


class UserViewSet(viewsets.ViewSet):

    def get_serializer_class(self):
        
        if self.action == "create":
            return UserCreateSerializer
        elif self.action == "update":
            return UserUpdateSerializer
        return UserSerializer

    @property
    def get_service(self):
        return AuthModuleRepositoryFactory.get_user_service(
            self.get_serializer_class()
        )

    def list(self, request):
        res = self.get_service.get_all()
        return Response(res)

    def retrieve(self, request, pk=None):
        res = self.get_service.get_by_id(pk)
        return Response(res)

    def create(self, request):
        serializer = self.get_serializer_class()
        
        validate_serializer = serializer(data=request.data)
        
        if validate_serializer.is_valid():
            data = self.get_service.create(validate_serializer.validated_data)
            return Response(data)
        return Response(validate_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        user_instance = self.get_service.repository.get_by_id(pk)
        
        if user_instance is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer_class()
        validate_serializer = serializer(user_instance, data=request.data)
        
        if validate_serializer.is_valid():
            updated_data = self.get_service.update(pk, validate_serializer.validated_data)
            return Response(updated_data)

        return Response(validate_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        res = self.get_service.delete(pk)
        return Response(res)
