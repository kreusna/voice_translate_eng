from . import views
from django.urls import path
from .views import (
    TodoListApiView,
    UploadViewSet,
)

urlpatterns = [
    path("test", views.index),
    path('api', TodoListApiView.as_view()),
    path('upload', UploadViewSet.as_view()),
]