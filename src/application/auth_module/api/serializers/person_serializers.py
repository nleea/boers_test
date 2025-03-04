from rest_framework import serializers
from src.application.auth_module.models import Person


class PersonSerializer(serializers.ModelSerializer):
    """Serializador para la entidad Person"""
    
    class Meta:
        model = Person
        fields = ["id", "fullname", "email"]
    
    def validate_email(self, value):
        """Valida que el email sea único."""
        if Person.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado.")
        return value