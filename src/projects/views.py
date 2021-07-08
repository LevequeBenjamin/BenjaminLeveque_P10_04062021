"""Docstrings."""

# lib
from itertools import chain

# django
from django.db import IntegrityError

# rest_framework
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

# models
from accounts.models import CustomUser
from projects.models import Project, Contributor, Issue, Comment

# permissions
from projects.permissions import IsAuthor, IsContributor, IsProjectAuthor, IsProjectContributor

# serializers
from projects.serializers import ProjectSerializer, ContributeurSerializer, IssueSerializer, CommentSerializer


class ProjectListCreateView(ListCreateAPIView):
    """
    Concrete view for listing a queryset or creating a Project instance.
    """
    serializer_class = ProjectSerializer
    # A user must be authenticated
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        """
        Override of the get_queryset method to return projects related to the authenticated user
        """
        contributor_projects = Project.objects.filter(author=self.request.user)
        author_projects = Project.objects.filter(contributors=self.request.user)
        set_projects = set(list(chain(contributor_projects, author_projects)))
        return set_projects

    def perform_create(self, serializer):
        """
        Override of the perform_create method to add the author.
        """
        serializer.save(author=self.request.user)


class ProjectUpdateDestroyDetailView(RetrieveUpdateDestroyAPIView):
    """
    Concrete view for retrieving, updating or deleting a Project instance.
    """
    serializer_class = ProjectSerializer
    # The user must be authenticated and the author of the project.
    permission_classes = [IsAuthenticated & IsAuthor]
    queryset = Project.objects.all()


class ContributorListCreateView(ListCreateAPIView):
    """
    Concrete view for listing a queryset or creating a Project instance.
    """
    serializer_class = ContributeurSerializer

    # A user must be authenticated
    @permission_classes([IsAuthenticated])
    def get_queryset(self, *args, **kwargs):
        """
        Override of the get_queryset method to return contributors related to the project.
        """
        return Contributor.objects.filter(project__id=self.kwargs.get('id_project'))

    # The user must be authenticated and the author of the project.
    @permission_classes([IsAuthenticated & IsProjectAuthor])
    def perform_create(self, serializer, *args, **kwargs):
        """
        Override of the perform_create method to add the projet and user instance.
        """
        user = CustomUser.objects.get(pk=self.request.data.get('user'))
        project = Project.objects.get(pk=self.kwargs.get('id_project'))
        if user == project.author:
            raise ValidationError("An author cannot be added as a contributor")
        try:
            serializer.save(project=project, user=user)
        except IntegrityError:
            raise ValidationError('This user is already a contributor')


class ContributorDestroyView(DestroyAPIView):
    """
    Concrete view for deleting a contributor instance.
    """
    serializer_class = ContributeurSerializer
    # The user must be authenticated, the contributor ou the author of the project.
    permission_classes = [IsAuthenticated & (IsContributor | IsProjectAuthor)]
    queryset = Contributor.objects.all()


class IssueListCreateView(ListCreateAPIView):
    """
    Concrete view for listing a queryset or creating a Issue instance.
    """
    serializer_class = IssueSerializer
    # The user must be authenticated, be part of the contributor ou the author of the project.
    permission_classes = [IsAuthenticated & (IsProjectContributor | IsProjectAuthor)]

    def get_queryset(self, *args, **kwargs):
        """
        Override of the get_queryset method to return issues related to the project.
        """
        return Issue.objects.filter(project__id=self.kwargs.get('id_project'))

    def perform_create(self, serializer, *args, **kwargs):
        """
        Override of the perform_create method to add the projet author and assignee.
        """
        project = Project.objects.get(pk=self.kwargs.get('id_project'))
        serializer.save(project=project, author=self.request.user, assignee=project.author)


class IssueUpdateDestroyDetailView(RetrieveUpdateDestroyAPIView):
    """
    Concrete view for retrieving, updating or deleting a Issue instance.
    """
    serializer_class = IssueSerializer
    # The user must be authenticated and the author of the issue.
    permission_classes = [IsAuthenticated & IsAuthor]
    queryset = Issue.objects.all()


class CommentListCreateView(ListCreateAPIView):
    """
    Concrete view for listing a queryset or creating a Comment instance.
    """
    serializer_class = CommentSerializer
    # The user must be authenticated, be part of the contributor ou the author of the project.
    permission_classes = [IsAuthenticated & (IsProjectContributor | IsProjectAuthor)]

    def get_queryset(self, *args, **kwargs):
        """
        Override of the get_queryset method to return comments related to the issue.
        """
        return Comment.objects.filter(issue__id=self.kwargs.get('id_issue'))

    def perform_create(self, serializer, *args, **kwargs):
        """
        Override of the perform_create method to add the issue and author.
        """
        issue = Issue.objects.get(pk=self.kwargs.get('id_issue'))
        serializer.save(issue=issue, author=self.request.user)


class CommentUpdateDestroyDetailView(RetrieveUpdateDestroyAPIView):
    """
    Concrete view for retrieving, updating or deleting a Comment instance.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated & IsAuthor]
    queryset = Comment.objects.all()
