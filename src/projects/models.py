"""Contains the models of projects app."""

# django
from django.contrib.auth import get_user_model
from django.db import models

# settings.AUTH_USER_MODEL
CustomUserModel = get_user_model()


class Project(models.Model):
    """
    This is a class allowing to create a Project.
    """
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1000)
    type = models.CharField(max_length=128)
    author = models.ForeignKey(
        to=CustomUserModel, on_delete=models.CASCADE, related_name='author_project'
    )
    contributors = models.ManyToManyField(CustomUserModel, through="Contributor")
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options."""
        ordering = ["-created_time"]
        verbose_name = "Project"

    def __str__(self):
        """Represents the class objects as a string."""
        return str(self.title)


class Contributor(models.Model):
    """
    This is a class allowing to create a Contributor.
    """
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=128)

    class Meta:
        """Meta options."""
        unique_together = ('user', 'project')

    def __str__(self):
        """Represents the class objects as a string."""
        return str(self.user)


class Issue(models.Model):
    """
    This is a class allowing to create a Issue.
    """
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1000)
    tag = models.CharField(max_length=128)
    priority = models.CharField(max_length=128)
    status = models.CharField(max_length=128)
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        to=CustomUserModel, on_delete=models.CASCADE, related_name='author_issue'
    )
    assignee = models.ForeignKey(
        to=CustomUserModel, on_delete=models.CASCADE, related_name='assignee'
    )
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='issue')

    class Meta:
        """Meta options."""
        ordering = ["-created_time"]
        verbose_name = "Issue"

    def __str__(self):
        """Represents the class objects as a string."""
        return str(self.title)


class Comment(models.Model):
    """
    This is a class allowing to create a Comment.
    """
    description = models.TextField(max_length=1000)
    author = models.ForeignKey(
        to=CustomUserModel, on_delete=models.CASCADE, related_name='author_comment'
    )
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE, related_name='comment')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options."""
        ordering = ["-created_time"]
        verbose_name = "Comment"
