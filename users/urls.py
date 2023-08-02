from django.urls import path
from .views import UserAPIView, SpartaTokenObtainPairView,SignupView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "users"

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/sparta/token/',SpartaTokenObtainPairView.as_view(),name='sparta_token'),
    path('signup/',SignupView.as_view(),name='signup'),
    path('login/',UserAPIView.as_view(), name='login'),
]