from rest_framework import serializers


class AuthSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class SchemaTokenLogin(serializers.Serializer):
    access = serializers.CharField(read_only=True, required=False)
    refresh = serializers.CharField(read_only=True, required=False)

class SchemaRequestLogin(serializers.Serializer):
    email = serializers.CharField(label='email or username')
    password = serializers.CharField()
    
class SchemaResponseLogin(serializers.Serializer):
    token = SchemaTokenLogin(read_only=True, required=False,source= "s")

class SchemaRequestForgetPassword(serializers.Serializer):
    email = serializers.CharField()

class SchemaRequestChangePassword(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField()
