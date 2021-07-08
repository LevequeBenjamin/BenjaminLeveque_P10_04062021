"""Docstrings."""

# django
from django.contrib.auth import get_user_model
from django.db import models

# settings.AUTH_USER_MODEL
CustomUserModel = get_user_model()


class Project(models.Model):
    """Docstrings."""
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1000)
    type = models.CharField(max_length=128)
    author = models.ForeignKey(to=CustomUserModel, on_delete=models.CASCADE, related_name='author_project')
    contributors = models.ManyToManyField(CustomUserModel, through="Contributor")


class Contributor(models.Model):
    """Docstrings."""
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=128)

    class Meta:
        unique_together = ('user', 'project')


class Issue(models.Model):
    """Docstrings."""
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1000)
    tag = models.CharField(max_length=128)
    priority = models.CharField(max_length=128)
    status = models.CharField(max_length=128)
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=CustomUserModel, on_delete=models.CASCADE, related_name='author_issue')
    assignee = models.ForeignKey(to=CustomUserModel, on_delete=models.CASCADE, related_name='assignee')
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='issue')


class Comment(models.Model):
    """Docstrings."""
    description = models.TextField(max_length=1000)
    author = models.ForeignKey(to=CustomUserModel, on_delete=models.CASCADE, related_name='author_comment')
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE, related_name='comment')
    created_time = models.DateTimeField(auto_now_add=True)