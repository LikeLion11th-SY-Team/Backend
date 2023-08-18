from django.urls import path
from .views import ProgressView

app_name = 'learnings'
urlpatterns = [
    path('update/', ProgressView.as_view(), name='progress_update'),
    path('get/', ProgressView.as_view(), name='progress_get'),
]