from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import CreateUserForm
from .decorators import unauthenticated_user
from .models import Profile


@unauthenticated_user
def loginView(request):
    """Login handler"""
    errorLogin = ""

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("bloggerHome", email=email)

        else:
            errorLogin = "Invalid email or password"

    context = {"error": errorLogin}
    return render(request, "login.html", context)


@unauthenticated_user
def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()

            name = request.POST.get("name")
            Profile.objects.create(user=user, name=name)

            login(request, user)
            return redirect("bloggerHome", kwargs={"email": user.email})

        else:
            print(form.errors.as_text())

    context = {}
    return render(request, "register.html", context)


def logoutView(request):
    """Logout user"""
    logout(request)
    return redirect("login")
