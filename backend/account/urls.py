from django.urls import path
from . import views

urlpatterns = [
    # ** Authentication
    path("login/", views.loginView, name="login"),
    path("logout/", views.logoutView, name="logout"),
    path("register/", views.register, name="register"),
    # **
    path("profile/", views.profile, name="profile"),
]
