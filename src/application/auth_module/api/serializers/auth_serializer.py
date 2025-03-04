from rest_framework import serializers


class AuthSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class SchemaTokenLogin(serializers.Serializer):
    access = serializers.CharField(read_only=True, required=False)
    refresh = serializers.CharField(read_only=True, required=False)


class SchemaResponseLogin(serializers.Serializer):
    token = SchemaTokenLogin(read_only=True, required=False,source= "s")
