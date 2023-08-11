from django.urls import path
<<<<<<< HEAD
from .views import UserAPIView, SpartaTokenObtainPairView,SignupView
# from .views import checkDuplicatedID,checkDuplicatedNickname
# from .views import getNickname,getUserInfo
=======
from .views import UserAPIView, SpartaTokenObtainPairView,SignupView,UserinfoView
from .views import checkDuplicatedID,checkDuplicatedNickname
from .views import getNickname
>>>>>>> 6aa5a4b ([FEAT] User 모델 수정 및 api 추가)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "users"

urlpatterns = [
    path('signup/',SignupView.as_view(),name='signup'),
    path('login/',UserAPIView.as_view(), name='login'),
    path('logout/',UserAPIView.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/sparta/token/',SpartaTokenObtainPairView.as_view(),name='sparta_token'),
<<<<<<< HEAD
    # path('api/check/id/',checkDuplicatedID,name='check_id'),
    # path('api/check/nickname/',checkDuplicatedNickname,name='check_Name'),
    # path('api/get/nickname/',getNickname,name='get_nickname'),
    # path('api/get/userinfo/',getUserInfo,name='get_userinfo'),
=======
    path('api/check/id/',checkDuplicatedID,name='check_id'),
    path('api/check/nickname/',checkDuplicatedNickname,name='check_Name'),
    path('api/get/nickname/',getNickname,name='get_nickname'),
    path('api/userinfo/',UserinfoView.as_view(),name='get_userinfo'),
>>>>>>> 6aa5a4b ([FEAT] User 모델 수정 및 api 추가)
]