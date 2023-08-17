from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    # 글 작성
    path('create/', views.PostView.as_view(), name='post_create'),

    # 글 안
    path('<int:post_pk>/delete/', views.PostView.as_view(), name='post_delete'),
    path('<int:post_pk>/update/', views.PostView.as_view(), name='post_update'),
    path('<int:post_pk>/like/', views.like_post, name='like_post'),
    path('<int:post_pk>/comments/', views.CommentView.as_view(), name='comments_create'),
    path('<int:post_pk>/', views.PostView.view_detail, name='post_detail'),

    # 글 목록
    path('<str:category>/', views.PostView.as_view(), name='post_list'),

    # 댓글 수정 삭제
    path('comments/<int:comment_pk>/delete/', views.CommentView.as_view(), name='comments_delete'),
    path('comments/<int:comment_pk>/update/', views.CommentView.as_view(), name='comments_update'),

]