"""
core/urls.py
"""

# Import necessary modules and classes
from django.urls import include, path

from .views import (
    RedisCacheTokensView,
    RefreshAccessTokenView,
    RegistrationView,
    UserLoginView,
    UserProileView,
)

# Define URL patterns specific to the 'core' app
urlpatterns = [
    # URL for user registration
    path("register/", RegistrationView.as_view(), name="register"),
    # URL for user login
    path("login/", UserLoginView.as_view(), name="login"),
    # URL for retrieving refresh tokens from Redis cache
    path(
        "redis-cache-tokens/",
        RedisCacheTokensView.as_view(),
        name="redis-cache-tokens",
    ),
    # URL for refreshing access tokens
    path(
        "refresh-access-token/",
        RefreshAccessTokenView.as_view(),
        name="refresh-access-token",
    ),
    # URL for retrieving user profiles
    path("user-profile/", UserProileView.as_view(), name="user-profiles"),
]
