from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


from .models import Post
from .forms import PostForm


@login_required(login_url="login")
def home(request):
    posts = Post.objects.all()

    context = {"posts": posts}
    return render(request, "home.html", context)


@login_required(login_url="login")
def createPost(request):
    form = PostForm()

    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user

            post.save()
            return redirect("home")

        else:
            print(form.errors.as_text())

    context = {
        "form": form,
    }
    return render(request, "postEdit.html", context)
