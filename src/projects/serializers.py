"""Docstrings."""

# rest_framework
from rest_framework import serializers

# accounts serializers
from accounts.serializers import CustomUserSerializer

# models
from projects.models import Project, Issue, Comment, Contributor


class ContributeurSerializer(serializers.ModelSerializer):
    """Docstrings."""
    user = CustomUserSerializer(read_only=True)

    class Meta:
        """Docstrings."""
        model = Contributor
        fields = ('id', 'user', 'role')


class CommentSerializer(serializers.ModelSerializer):
    """Docstrings."""
    author = CustomUserSerializer(read_only=True)

    class Meta:
        """Docstrings."""
        model = Comment
        fields = ('id', 'description', 'author', 'created_time')


class IssueSerializer(serializers.ModelSerializer):
    """Docstrings."""
    comments = CommentSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    assignee = CustomUserSerializer(read_only=True)

    class Meta:
        """Docstrings."""
        model = Issue
        fields = ('id', 'title', 'description', 'tag', 'priority', 'status', "created_time",
                  'author', 'assignee', 'comments')


class ProjectSerializer(serializers.ModelSerializer):
    """Docstrings."""
    issues = IssueSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    contributors = CustomUserSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        """Docstrings."""
        model = Project
        fields = ('id', 'title', 'description', 'type', 'author', 'contributors', 'issues', 'comments')
