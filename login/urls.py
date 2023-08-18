from django.urls import path
from .views import KakaoLoginView

urlpatterns = [
    path('api/kakao-login/', KakaoLoginView.as_view(), name='kakao-login'),
]             