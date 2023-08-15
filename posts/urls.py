from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.Posts, name='post_list'),
    path('<int:post_pk>/comments/', views.CommentView.as_view(), name='comments_create'),
    path('comments/<int:comment_pk>/delete/', views.CommentView.as_view(), name='comments_delete'),
    path('comments/<int:comment_pk>/update/', views.CommentView.as_view(), name='comments_update'),
    path('<int:post_pk>/like/', views.like_post, name='like_post'),
]