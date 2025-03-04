from rest_framework import serializers
from django.contrib.auth import authenticate

class AuthValidator(serializers.Serializer):
    email = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField()
    
    def validate(self, attrs):
    
        data = {}
        if 'email' in attrs:
            data["username"] = attrs.get("email",None)
            data["password"] = attrs.get("password",None)
        else:
            data = attrs
        
        user = authenticate(**data)
        
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials Passed.")