from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('<int:post_pk>/comments/', views.CommentView.as_view(), name='comments_create'),
    path('comments/<int:comment_pk>/delete/', views.CommentView.as_view(), name='comments_delete'),
    path('comments/<int:comment_pk>/update/', views.CommentView.as_view(), name='comments_update'),
    path('<int:post_pk>/like/', views.like_post, name='like_post'),

    
    path('board/create/', views.PostView.as_view(), name='post_create'),
    path('board/<int:post_pk>/delete/', views.PostView.as_view(), name='post_delete'),
    path('board/<int:post_pk>/update/', views.PostView.as_view(), name='post_update'),
    path('board/<int:post_pk>/', views.PostView.view_detail, name='post_detail'),
    path('board/<str:category>/', views.PostView.as_view(), name='post_list'),
    
]