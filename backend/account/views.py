from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm, ProfileForm
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
            return redirect("bloggerHome", user.email)

        else:
            print(form.errors.as_text())

    context = {}
    return render(request, "register.html", context)


@login_required(login_url="login")
def logoutView(request):
    """Logout user"""
    logout(request)
    return redirect("home")


@login_required(login_url="login")
def profile(request):
    """Profile"""
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        print(request.POST, request.FILES)
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
        else:
            print(form.errors.as_text())

    context = {"profile": profile}
    return render(request, "profile.html", context)
