from rest_framework import serializers
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create and return user wth encrypted password"""
        return User.objects.create_user(**validated_data)
# overriding jwt creation serializer in djoser to return custom response
