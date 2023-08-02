from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    # FBV로 단순 request 처리 및 페이지 render 하는 형태
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('signup/', views.signupView, name='signup'),
    
    # CBV로 json 형태로 받아서 POST 시 Json 형태의 response만 응답할 때
    # POST 요청에서 페이지 render X
    path('login2/', views.LoginView.as_view()),
    path('signup2/', views.SignupView.as_view()),
]