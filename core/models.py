"""
core/models.py
"""

import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


# Custom User Manager to handle user creation and superuser creation
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, password2=None):
        """
        Creates and saves a User with the given email, first_name, last_name and password.
        """
        # Validate that the email is provided
        if not email:
            raise ValueError("User must have an email address")

        # Create a new user instance
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        # Set the user's password
        user.set_password(password)
        # Save the user to the database
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given email, first_name, last_name and password.
        """
        # Create a regular user using the create_user method
        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        # Set the superuser flag to True
        user.is_superuser = True
        # Save the superuser to the database
        user.save(using=self._db)
        return user


# Custom User model that extends AbstractUser
class User(AbstractUser):
    # Add a UUID field for uniqueness
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # Email field with a maximum length of 255 characters
    email = models.EmailField(max_length=255, unique=True)
    # First name field with a maximum length of 255 characters
    first_name = models.CharField(max_length=255)
    # Last name field with a maximum length of 255 characters
    last_name = models.CharField(max_length=255)
    # Flag to determine if the user is a superuser
    is_superuser = models.BooleanField(default=False)
    # Use the custom UserManager for managing user objects
    objects = UserManager()
    # Remove the username field and use email as the unique identifier
    username = None
    USERNAME_FIELD = "email"
    # Additional required fields for user creation
    REQUIRED_FIELDS = ["first_name", "last_name"]

    # Define a string representation for the User model
    def __str__(self):
        return self.first_name

    # Check if the user has a specific permission
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always for superusers
        return self.is_superuser

    # Check if the user is a member of staff
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser

    # Override the save method to call the parent class's save method
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
