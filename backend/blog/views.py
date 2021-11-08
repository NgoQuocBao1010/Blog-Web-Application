from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import pytz
from datetime import timezone

from .models import Post, Category
from .forms import PostForm, CommentForm

User = get_user_model()


def home(request):
    """Home page, where user and unauth user can view all the posts"""
    posts = Post.objects.all()
    posts = filterPosts(request, posts)
    popularPosts = Post.objects.annotate(num_comment=Count("comment")).order_by(
        "-num_comment"
    )[:5]

    categories = Category.objects.all()

    context = {"posts": posts, "categories": categories, "popularPosts": popularPosts}
    return render(request, "home.html", context)


def bloggerHome(request, email):
    """Home of individual blogger"""

    try:
        blogger = User.objects.get(email=email)
    except User.DoesNotExist:
        return HttpResponse("Not exist")

    posts = Post.objects.filter(author=blogger)
    posts = filterPosts(request, posts)
    popularPosts = posts.annotate(num_comment=Count("comment")).order_by(
        "-num_comment"
    )[:5]

    categories = Category.objects.filter(post__author=blogger).annotate(
        total=Count("post")
    )

    context = {
        "blogger": blogger,
        "posts": posts,
        "categories": categories,
        "popularPosts": popularPosts,
    }
    return render(request, "my-blog.html", context)


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


def postDetail(request, id):
    """Post detail view, user can post comment to post here"""
    post = get_object_or_404(Post, id=id)
    categories = Category.objects.all()
    popularPosts = Post.objects.annotate(num_comment=Count("comment")).order_by(
        "-num_comment"
    )[:5]

    context = {
        "post": post,
        "categories": categories,
        "popularPosts": popularPosts,
    }
    return render(request, "postDetail.html", context)


@login_required(login_url="login")
def postDelete(request, id):
    """Delete a post, only if user is the author"""
    post = Post.objects.get(id=id)

    if post.author != request.user:
        return render(request, "unauthorized.html", {})

    post.delete()
    return redirect("home")


# AJAX connection
@csrf_exempt
def newComment(request):
    """Handle ajax request to create new comment"""
    if request.is_ajax and request.method == "POST":
        responseData = {}

        postId = request.POST.get("postId")
        post = Post.objects.get(id=postId)

        form = CommentForm(request.POST)
        if form.is_valid():
            newComment = form.save(commit=False)
            newComment.commentor = (
                request.user if request.user.is_authenticated else None
            )
            newComment.post = post
            newComment.save()

            # Response data
            commentor = (
                "Guest" if not newComment.commentor else newComment.commentor.email
            )

            localDatetime = newComment.dateCreated.replace(tzinfo=timezone.utc)
            local_tz = "Asia/Ho_Chi_Minh"
            localDatetime = localDatetime.astimezone(pytz.timezone(local_tz))
            formatDate = (
                localDatetime.strftime("%b. %d, %Y, %I:%M %p")
                .replace("AM", "a.m.")
                .replace("PM", "p.m.")
                .replace(". 0", ". ")
                .replace(", 0", ", ")
            )

            responseData.update(
                {
                    "commentor": commentor,
                    "dateCreated": formatDate,
                    "content": request.POST.get("content"),
                }
            )

        else:
            print(form.errors.as_text())

    return JsonResponse(responseData, status=200)


def filterPosts(request, posts):
    """Filter post on get request"""
    category = request.GET.get("category")
    if category:
        posts = posts.filter(category__name__icontains=category)

    return posts


# print(request.resolver_match.view_name)
