"""SoftDesk URL Configuration."""

# django
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # admin
    path('api/admin/', admin.site.urls),
    # accounts
    path('api/', include("accounts.urls")),
    # projects
    path('api/', include("projects.urls")),
]
