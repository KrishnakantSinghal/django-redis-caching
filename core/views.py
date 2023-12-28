"""
core/views.py
"""

from django.conf import settings
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
# Import necessary modules and classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserRegisterSerializer,
    UserSerializer,
)


# View for user registration
class RegistrationView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request):
        """
        Create a user account
        """
        # Extract and validate email from the request data
        email = request.data.get("email").lower()
        try:
            # Check if an account with the given email already exists
            User.objects.get(email=email)
            return Response(
                {"errors": "An account with the given email already exists"},
                status=status.HTTP_403_FORBIDDEN,
            )
        except User.DoesNotExist:
            pass

        # Create a new user using the provided data
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate tokens for the newly registered user
            token_serializer = CustomTokenObtainPairSerializer()
            tokens = token_serializer.get_token(user)

            # Set tokens in cache with an expiration time (adjust as needed)
            cache.set(user.uuid, tokens["refresh"], timeout=3600)  # 1 hour

            # Include the tokens in the response if needed
            response_data = {
                "uuid": user.uuid,
                "msg": "Registration Successful, Email verification link sent. Please verify your email.",
                "email": email,
                "refresh_token": tokens["refresh"],
                "access_token": tokens["access"],
            }

            return Response({"code": 201, "data": response_data}, status=status.HTTP_201_CREATED)

        return Response(
            {"code": 403, "errors": serializer.errors},
            status=status.HTTP_403_FORBIDDEN,
        )


# View for user login
class UserLoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, format=None):
        """
        This method is used to login.
        """
        # Extract and validate email and password from the request data
        email = request.data.get("email").lower()
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            token = self.serializer_class.get_token(user)

            # Set tokens in cache with an expiration time (adjust as needed)
            cache.set(user.uuid, token["refresh"], timeout=3600)  # 1 hour

            response_dict = {"uuid": user.uuid, "token": token, "msg": "Login Success"}
            return Response({"code": 200, "data": response_dict}, status=status.HTTP_200_OK)
        return Response(
            {"code": 404, "errors": "Email or Password is not Valid"},
            status=status.HTTP_404_NOT_FOUND,
        )


# View for retrieving all user profiles
class UserProileView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        returns all users information
        """
        queryset = User.objects.all()
        return queryset


# View for retrieving the refresh token from Redis cache
class RedisCacheTokensView(GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        getting refresh token from redis cache
        """
        # Extract UUID from the request data
        uuid = request.GET.get("uuid")
        token = cache.get(uuid)
        if token:
            response_dict = {"refresh_token": token}
            return Response({"code": 200, "data": response_dict}, status=status.HTTP_200_OK)
        return Response(
            {"code": 404, "errors": "Your tokens may not present"},
            status=status.HTTP_404_NOT_FOUND,
        )


# View for refreshing an access token
class RefreshAccessTokenView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        """
        refresh an access token
        """
        # Extract refresh token and UUID from the request data
        refresh_token = request.data.get("refresh_token")
        uuid = request.data.get("uuid")
        try:
            user_token = cache.get(uuid)
            if user_token:
                if refresh_token:
                    # Attempt to refresh the access token using the provided refresh token
                    refresh = RefreshToken(refresh_token)
                    access_token = str(refresh.access_token)
                    return Response({"access_token": access_token}, status=status.HTTP_200_OK)
                return Response(
                    {"code": 403, "error": "Please enter a refresh token"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            return Response(
                {
                    "code": 404,
                    "error": "Refresh token not available in cache or invalid uuid",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except TokenError:
            cache.delete(uuid)
            return Response(
                {"code": 400, "error": "Token is invalid or expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
