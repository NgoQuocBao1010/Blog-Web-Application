from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

from .forms import CreateUserForm
from .decorators import unauthenticated_user


@unauthenticated_user
def loginView(request):
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
    return render(request, 'login.html', context)


@unauthenticated_user
def register(request):
    if request.method == "POST":
        print(request.POST)
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

        else:
            print(form.errors)
    
    context = {}
    return render(request, 'register.html', context)

