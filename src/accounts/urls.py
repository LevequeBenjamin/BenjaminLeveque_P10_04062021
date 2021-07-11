"""Contains the urls of accounts app."""

# django
from django.urls import path, include

# rest_framework
from rest_framework_simplejwt import views as jwt_views

# views
from accounts.views import CustomUserListView, LogoutView, CustomUserRetrieveUpdateView,\
    CustomUserUpdatePasswordView, CustomUserDestroyView

urlpatterns = [
    # POST
    path('signup/', include('rest_auth.registration.urls'), name='signup'),
    # POST
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='login'),
    # POST
    path('logout/', LogoutView.as_view(), name='logout'),
    # POST
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # GET
    path('users/', CustomUserListView.as_view(), name='users'),
    # GET, PUT
    path('users/<int:pk>/', CustomUserRetrieveUpdateView.as_view(), name='retrieve_update_user'),
    # PUT
    path(
        'users/<int:pk>/new-password/', CustomUserUpdatePasswordView.as_view(),
        name='update_password_user'
    ),
    # DELETE
    path('users/<int:pk>/delete-user/', CustomUserDestroyView.as_view(), name='delete_user'),
]
