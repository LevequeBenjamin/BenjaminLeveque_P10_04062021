"""Contains the views of projects app."""

# lib
from itertools import chain

# django
from django.db import IntegrityError

# rest_framework
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,\
    DestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

# models
from accounts.models import CustomUser
from projects.models import Project, Contributor, Issue, Comment

# permissions
from projects.permissions import IsAuthor, IsProjectAuthor, IsProjectContributor,\
    IsAuthorOrContributor

# serializers
from projects.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer,\
    CommentSerializer


class ProjectListCreateView(ListCreateAPIView):
    """
    Concrete view for listing a queryset or creating a Project instance.
    """
    serializer_class = ProjectSerializer
    # A user must be authenticated
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Override of the get_queryset method to return projects related to the authenticated user.
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


class ProjectRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Concrete view for retrieving, updating or deleting a Project instance.
    """
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    # The user must be authenticated, the author of the issue or admin.
    permission_classes = [IsAuthenticated, IsAuthor]


class ContributorListCreateView(ListCreateAPIView):
    """
    Concrete view for listing a queryset or creating a Project instance.
    """
    serializer_class = ContributorSerializer
    # The user must be authenticated, be part of the contributor ou the author of the project.
    permission_classes = [IsAuthenticated, IsProjectAuthor]

    def get_queryset(self):
        """
        Override of the get_queryset method to return contributors related to the project.
        """
        return Contributor.objects.filter(project__id=self.kwargs.get('id_project'))

    def perform_create(self, serializer):
        """
        Override of the perform_create method to add the projet and user instance.
        """
        user = get_object_or_404(CustomUser, pk=self.request.data.get("user"))
        project = get_object_or_404(Project, pk=self.kwargs.get("id_project"))
        if user == project.author:
            raise ValidationError("An author cannot be added as a contributor")
        try:
            serializer.save(project=project, user=user)
        except IntegrityError as err:
            raise ValidationError('This user is already a contributor') from err


class ContributorDestroyView(DestroyAPIView):
    """
    Concrete view for deleting a contributor instance.
    """
    serializer_class = ContributorSerializer
    # The user must be authenticated, the contributor ou the author of the project.
    permission_classes = [IsAuthenticated, IsProjectAuthor]
    queryset = Contributor.objects.all()


class IssueListCreateView(ListCreateAPIView):
    """
    Concrete view for listing a queryset or creating a Issue instance.
    """
    serializer_class = IssueSerializer
    # The user must be authenticated, be part of the contributor ou the author of the project.
    permission_classes = [IsAuthenticated, IsProjectContributor]

    def get_queryset(self):
        """
        Override of the get_queryset method to return issues related to the project.
        """
        return Issue.objects.filter(project__id=self.kwargs.get('id_project'))

    def perform_create(self, serializer):
        """
        Override of the perform_create method to add the projet author and assignee.
        """
        project = get_object_or_404(Project, pk=self.kwargs.get("id_project"))
        serializer.save(project=project, author=self.request.user, assignee=project.author)


class IssueRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Concrete view for retrieving, updating or deleting a Issue instance.
    """
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()
    # The user must be authenticated, be part of the contributor ou the author of the project.
    permission_classes = [IsAuthenticated, IsAuthorOrContributor]


class CommentListCreateView(ListCreateAPIView):
    """
    Concrete view for listing a queryset or creating a Comment instance.
    """
    serializer_class = CommentSerializer
    # The user must be authenticated, be part of the contributor ou the author of the project.
    permission_classes = [IsAuthenticated, IsProjectContributor]

    def get_queryset(self):
        """
        Override of the get_queryset method to return comments related to the issue.
        """
        return Comment.objects.filter(issue__id=self.kwargs.get('id_issue'))

    def perform_create(self, serializer):
        """
        Override of the perform_create method to add the issue and author.
        """
        issue = get_object_or_404(Issue, pk=self.kwargs.get("id_issue"))
        serializer.save(issue=issue, author=self.request.user)


class CommentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Concrete view for retrieving, updating or deleting a Comment instance.
    """
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsAuthorOrContributor]
