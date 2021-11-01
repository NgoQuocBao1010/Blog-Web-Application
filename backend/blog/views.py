from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required(login_url="login")
def home(request):

    return render(request, 'home.html', {})



def logoutView(request):
    logout(request)
    return redirect('login')
