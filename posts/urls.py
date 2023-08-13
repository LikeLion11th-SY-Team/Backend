from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    
    path('<int:post_pk>/comments/', views.CommentView.as_view(), name='comments_create'),
    path('<int:post_pk>/comments/<int:comment_pk>/delete/', views.CommentView.as_view(), name='comments_delete'),
]