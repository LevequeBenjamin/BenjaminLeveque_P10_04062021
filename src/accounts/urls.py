from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from accounts.views import CustomUserListView, CustomUserDetailView

urlpatterns = [
    path('signup/', include('rest_auth.registration.urls')),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='rest_login'),
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('rest_auth.urls')),
    path('users/', CustomUserListView.as_view()),
    path('users/<int:pk>/', CustomUserDetailView.as_view()),
]
