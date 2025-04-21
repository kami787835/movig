from django.urls import path
from . import views

urlpatterns = [
    path("admin", views.MovieAPIView.as_view()),
]
