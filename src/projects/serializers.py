"""Contains the serializers of projects app."""

# rest_framework
from rest_framework import serializers

# accounts serializers
from accounts.serializers import CustomUserSerializer

# models
from projects.models import Project, Issue, Comment, Contributor


class ContributorSerializer(serializers.ModelSerializer):
    """
    Allows to serialize or deserialize the contributor according
    to the verb of the request.
    """
    user = CustomUserSerializer(read_only=True)

    class Meta:
        """Meta options."""
        model = Contributor
        fields = ('id', 'user', 'role')


class CommentSerializer(serializers.ModelSerializer):
    """
    Allows to serialize or deserialize the comment according
    to the verb of the request.
    """
    author = CustomUserSerializer(read_only=True)

    class Meta:
        """Meta options."""
        model = Comment
        fields = ('id', 'description', 'author', 'created_time')


class IssueSerializer(serializers.ModelSerializer):
    """
    Allows to serialize or deserialize the issue according
    to the verb of the request.
    """
    comments = CommentSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    assignee = CustomUserSerializer(read_only=True)

    class Meta:
        """Meta options."""
        model = Issue
        fields = ('id', 'title', 'description', 'tag', 'priority', 'status', "created_time",
                  'author', 'assignee', 'comments')


class ProjectSerializer(serializers.ModelSerializer):
    """
    Allows to serialize or deserialize the project according
    to the verb of the request.
    """
    issues = IssueSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    contributors = CustomUserSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        """Meta options."""
        model = Project
        fields = (
            'id', 'title', 'description', 'type', 'author',
            'contributors', 'issues', 'comments', 'created_time',
        )
