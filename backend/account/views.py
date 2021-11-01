from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
import json

from .forms import CreateUserForm
from .decorators import unauthenticated_user


@unauthenticated_user
def loginView(request):
    """ Login handler """
    errorLogin = ""

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

        else:
            errorLogin = "Invalid email or password"

    context = {"error": errorLogin}
    return render(request, "login.html", context)


@unauthenticated_user
def register(request):
    errorMsg = None

    if request.method == "POST":
        print(request.POST)
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

        else:
            errorMsg = form.errors.as_json()

    context = {"error": errorMsg}
    return render(request, "register.html", context)


def logoutView(request):
    """ Logout user """
    logout(request)
    return redirect("login")
