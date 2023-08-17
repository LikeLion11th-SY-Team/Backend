from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.Posts, name='post_list'),
    path('<int:post_pk>/comments/', views.CommentView.as_view(), name='comments_create'),
    path('comments/<int:comment_pk>/delete/', views.CommentView.as_view(), name='comments_delete'),
    path('comments/<int:comment_pk>/update/', views.CommentView.as_view(), name='comments_update'),
    path('<int:post_pk>/like/', views.like_post, name='like_post'),

    path('board/<str:category>/', views.PostListView.as_view(), name='post_list'),
    path('board/<str:category>/create/', views.PostCreateView.as_view(), name='post_create'),
    path('board/<str:category>/<int:post_pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('board/<str:category>/<int:post_pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('board/<str:category>/<int:post_pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]