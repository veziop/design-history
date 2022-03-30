import re

from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser object.
    """

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update an existing user and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

    def validate_password(self, password):
        """Validate the password is formated correctly and return it"""
        if len(password) < 8:
            raise serializers.ValidationError("Password must be longer than 8 characters")
        # pattern = bool(re.match(r'[a-z]+]', password)) and bool(re.match(r'[0-9]+'))

        # if re.match(r'[a-zA-Z0-9]+$', password):
        if not bool(re.search(r'[0-9]', password) and re.search(r'[a-zA-Z]', password)):
            raise serializers.ValidationError("Password must contain one letter character and one number character")
        return password
