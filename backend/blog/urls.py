from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("post/", views.createPost, name="createPost"),
    path("post/<str:id>/", views.postDetail, name="postDetail"),
    path("post/<str:id>/delete", views.postDelete, name="postDelete"),
    path("post/<str:id>/edit", views.postEdit, name="postEdit"),
    # AJAX request
    path("post/ajax/comment", views.testingAjax, name="postComment"),
]
