"""
config/urls.py
"""

import debug_toolbar

# Import necessary modules and classes
from django.contrib import admin
from django.urls import include, path

# Define project-level URL patterns
urlpatterns = [
    # Include Django Debug Toolbar URLs for debugging purposes
    path("__debug__/", include(debug_toolbar.urls)),
    # Default Django Admin URLs
    path("admin/", admin.site.urls),
    # Include application-specific URLs from the 'core' app
    path("", include("core.urls")),
]
