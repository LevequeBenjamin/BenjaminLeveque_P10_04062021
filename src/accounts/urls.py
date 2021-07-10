from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from accounts.views import CustomUserListView, LogoutView, CustomUserRetrieveUpdateView, CustomUserUpdatePasswordView, \
    CustomUserDestroyView

urlpatterns = [
    path('signup/', include('rest_auth.registration.urls'), name='signup'),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', CustomUserListView.as_view()),
    path('users/<int:pk>/', CustomUserRetrieveUpdateView.as_view()),
    path('users/<int:pk>/new-password/', CustomUserUpdatePasswordView.as_view()),
    path('users/<int:pk>/delete-user/', CustomUserDestroyView.as_view()),
]
