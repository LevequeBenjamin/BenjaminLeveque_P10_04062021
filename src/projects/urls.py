"""Contains the urls of projects app."""

# django
from django.urls import path

# views
from projects.views import ProjectListCreateView, ProjectUpdateDestroyDetailView, \
    ContributorDestroyView, ContributorListCreateView, IssueListCreateView,\
    IssueUpdateDestroyDetailView, CommentListCreateView, CommentUpdateDestroyDetailView

urlpatterns = [
    # project
    # GET, POST
    path('projects/', ProjectListCreateView.as_view()),
    # GET, PUT, PATCH, DELETE
    path('projects/<int:pk>/', ProjectUpdateDestroyDetailView.as_view()),

    # contributor
    # GET, POST
    path('projects/<int:id_project>/users/', ContributorListCreateView.as_view()),
    # DELETE
    path('projects/<int:id_project>/users/<int:pk>/', ContributorDestroyView.as_view()),

    # issue
    # GET, POST
    path('projects/<int:id_project>/issues/', IssueListCreateView.as_view()),
    # PUT, DELETE
    path(
        'projects/<int:id_project>/issues/<int:pk>/', IssueUpdateDestroyDetailView.as_view()
    ),

    # comment
    # GET, POST
    path(
        'projects/<int:id_project>/issues/<int:id_issue>/comments/', CommentListCreateView.as_view()
    ),
    path('projects/<int:id_project>/issues/<int:id_issue>/comments/<int:pk>/',
         CommentUpdateDestroyDetailView.as_view()),

]
