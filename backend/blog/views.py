from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


from .models import Post, Category
from .forms import PostForm


@login_required(login_url="login")
def home(request):
    """ Home page, where user can view all the posts """
    posts = Post.objects.all()
    categories = Category.objects.all()
    
    context = {"posts": posts, "categories": categories}
    return render(request, "home.html", context)


@login_required(login_url="login")
def createPost(request):
    form = PostForm()

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

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
