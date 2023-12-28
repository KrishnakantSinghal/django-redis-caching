"""
core/serializers.py
"""

# Import necessary modules and classes
from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# Custom serializer for obtaining JWT tokens with additional user information
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Call the parent class's get_token method
        token = super().get_token(user)

        # Add custom claims to the token
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["email"] = user.email

        # Save the refresh token to the user model
        user.refresh_token = str(token)
        user.save()

        # Return a dictionary containing refresh and access tokens
        return {
            "refresh": str(token),
            "access": str(token.access_token),
        }


# Serializer for user registration
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        # Use the User model and specify the fields to include in the serializer
        model = User
        fields = ["email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        # Create a new user using the provided data
        user = User.objects.create(**validated_data)
        # Set the user's password
        user.set_password(validated_data.get("password"))
        return user


# Serializer for user details (excluding the password field)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # Use the User model and exclude the password field from serialization
        model = User
        exclude = ["password"]
