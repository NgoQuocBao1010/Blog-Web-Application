from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count


from .models import Post, Category
from .forms import PostForm, CommentForm


@login_required(login_url="login")
def home(request):
    """Home page, where user can view all the posts"""
    posts = Post.objects.all()
    categories = Category.objects.all()

    popularPosts = Post.objects.annotate(num_comment=Count("comment")).order_by(
        "-num_comment"
    )[:5]

    context = {"posts": posts, "categories": categories, "popularPosts": popularPosts}
    return render(request, "home.html", context)


@login_required(login_url="login")
def createPost(request):
    """Create a new post"""
    form = PostForm()

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            post.save()
            return redirect("postDetail", id=post.id)

        else:
            print(form.errors.as_text())

    context = {
        "form": form,
    }
    return render(request, "postEdit.html", context)


@login_required(login_url="login")
def postEdit(request, id):
    """Edit a post, only if user is the author"""
    post = Post.objects.get(id=id)

    if request.user != post.author:
        return render(request, "unauthorized.html", {})

    form = PostForm(instance=post)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            post = form.save()
            return redirect("postDetail", id=id)

        else:
            print(form.errors.as_text())

    context = {
        "form": form,
    }
    return render(request, "postEdit.html", context)


@login_required(login_url="login")
def postDetail(request, id):
    """Post detail view, user can post comment to post here"""
    post = get_object_or_404(Post, id=id)

    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            newComment = form.save(commit=False)
            newComment.commentor = request.user
            newComment.post = post

            newComment.save()
            return redirect("postDetail", id=id)

        else:
            print(form.errors.as_text())

    context = {"post": post, "form": form}
    return render(request, "post.html", context)


@login_required(login_url="login")
def postDelete(request, id):
    """Delete a post, only if user is the author"""
    post = Post.objects.get(id=id)

    if post.author != request.user:
        return render(request, "unauthorized.html", {})

    post.delete()
    return redirect("home")
