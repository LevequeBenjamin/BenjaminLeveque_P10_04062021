from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from accounts.views import CustomUserListView, LogoutView, CustomUserRetrieveView, CustomUserUpdatePasswordView, \
    CustomUserDestroyView

urlpatterns = [
    path('signup/', include('rest_auth.registration.urls'), name='signup'),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', CustomUserListView.as_view()),
    path('users/<int:pk>/', CustomUserRetrieveView.as_view()),
    path('users/<int:pk>/newPassword/', CustomUserUpdatePasswordView.as_view()),
    path('users/<int:pk>/deleteUser/', CustomUserDestroyView.as_view()),
]
