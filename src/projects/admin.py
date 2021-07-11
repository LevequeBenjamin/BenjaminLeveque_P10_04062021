"""Customizing the administrator interface."""

# django
from django.contrib import admin

# models
from projects.models import Project, Issue, Comment

admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Comment)
