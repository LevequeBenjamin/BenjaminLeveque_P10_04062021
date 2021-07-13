"""Contains the urls of projects app."""

# django
from django.urls import path

# views
from projects.views import ProjectListCreateView, ProjectRetrieveUpdateDestroyView, \
    ContributorDestroyView, ContributorListCreateView, IssueListCreateView, \
    IssueRetrieveUpdateDestroyView, CommentListCreateView, CommentRetrieveUpdateDestroyView

urlpatterns = [
    # project
    # GET, POST
    path('projects/', ProjectListCreateView.as_view(), name="list_create_project"),
    # GET, PUT, PATCH, DELETE
    path('projects/<int:pk>/', ProjectRetrieveUpdateDestroyView.as_view(),
         name="update_destroy_retrieve_project"),

    # contributor
    # GET, POST
    path('projects/<int:id_project>/users/', ContributorListCreateView.as_view(),
         name="list_create_contributor"),
    # DELETE
    path('projects/<int:id_project>/users/<int:pk>/', ContributorDestroyView.as_view(),
         name="delete_contributor"),

    # issue
    # GET, POST
    path('projects/<int:id_project>/issues/', IssueListCreateView.as_view(),
         name="list_create_issue"),
    # PUT, DELETE
    path(
        'projects/<int:id_project>/issues/<int:pk>/', IssueRetrieveUpdateDestroyView.as_view(),
        name="update_destroy_issue"
    ),

    # comment
    # GET, POST
    path(
        'projects/<int:id_project>/issues/<int:id_issue>/comments/', CommentListCreateView.as_view(),
        name="list_create_comment"
    ),
    path('projects/<int:id_project>/issues/<int:id_issue>/comments/<int:pk>/',
         CommentRetrieveUpdateDestroyView.as_view(), name="update_destroy_retrieve_comment"),
]
