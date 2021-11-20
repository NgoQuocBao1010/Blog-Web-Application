from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings

import os
import pytz
from datetime import timezone
from PIL import Image
import shortuuid

from .models import Post, Category, Comment
from .forms import PostForm, CommentForm

User = get_user_model()


def home(request):
    """Home page, where user and unauth user can view all the posts"""
    posts = Post.objects.all()
    posts, tags, queryPath = filterPosts(request, posts)
    popularPosts = Post.objects.annotate(num_comment=Count("comment")).order_by(
        "-num_comment"
    )[:5]

    categories = Category.objects.all()
    posts = pagination(request, posts)

    context = {
        "posts": posts,
        "categories": categories,
        "tags": tags,
        "queryPath": queryPath,
        "popularPosts": popularPosts,
    }
    return render(request, "home.html", context)


def bloggerHome(request, email):
    """Home of individual blogger"""
    try:
        blogger = User.objects.get(email=email)
    except User.DoesNotExist:
        return HttpResponse("Not exist")

    posts = Post.objects.filter(author=blogger)
    posts, tags, queryPath = filterPosts(request, posts)

    # Query 5 most popular posts depends on the number of comments
    popularPosts = posts.annotate(num_comment=Count("comment")).order_by(
        "-num_comment"
    )[:5]

    # Query and counts the number of post per category
    categories = Category.objects.filter(post__author=blogger).annotate(
        total=Count("post")
    )

    posts = pagination(request, posts)

    context = {
        "blogger": blogger,
        "posts": posts,
        "tags": tags,
        "queryPath": queryPath,
        "categories": categories,
        "popularPosts": popularPosts,
    }
    return render(request, "my-blog.html", context)


def postDetail(request, id):
    """Post detail view, user can post comment to post here"""
    if request.method == "GET" and request.GET.get("search"):
        return home(request)

    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return HttpResponse("This page does not exist")

    blogger = post.author
    categories = Category.objects.all()
    popularPosts = (
        Post.objects.filter(author=post.author)
        .annotate(num_comment=Count("comment"))
        .order_by("-num_comment")[:5]
    )

    relatedPosts = getRelatedPost(post)

    context = {
        "blogger": blogger,
        "post": post,
        "categories": categories,
        "popularPosts": popularPosts,
        "relatedPosts": relatedPosts,
    }
    return render(request, "postDetail.html", context)


@login_required(login_url="login")
def postCustomize(request):
    """Create a new post"""
    posts = Post.objects.filter(author=request.user)

    context = {"posts": posts}
    return render(request, "postCustom.html", context)


@login_required(login_url="login")
def postCreate(request):
    """Create a new post"""
    form = PostForm()
    categories = Category.objects.all()

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            category = categoryHandler(request)
            post.category = category

            post.save()
            return redirect("postDetail", id=post.id)
        else:
            print(form.errors.as_text())

    context = {"categories": categories, "form": form}
    return render(request, "postCreate.html", context)


@login_required(login_url="login")
def postEdit(request, id):
    """Edit a post, only if user is the author"""
    categories = Category.objects.all()
    post = Post.objects.get(id=id)

    if request.user != post.author:
        return render(request, "unauthorized.html", {})

    form = PostForm(instance=post)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            post = form.save()
            category = categoryHandler(request)
            post.category = category

            post.save()
            return redirect("postDetail", id=id)
        else:
            print(form.errors.as_text())

    context = {"post": post, "categories": categories}
    return render(request, "postEdit.html", context)


@login_required(login_url="login")
def postDelete(request, id):
    """Delete a post, only if user is the author"""
    post = Post.objects.get(id=id)

    if post.author != request.user:
        return render(request, "unauthorized.html", {})

    post.delete()
    return redirect("postCustomize")


""" AJAX connection """


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
            responseData = commentResponseData(newComment, request)

        else:
            print(form.errors.as_text())

    return JsonResponse(responseData, status=200)


@csrf_exempt
def deleteComment(request, id):
    """Delete comment"""
    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        return JsonResponse(data={"error": "not success"}, status=404)

    if request.is_ajax and request.method == "DELETE":
        comment.delete()

    return JsonResponse(data={"message": "success"}, status=200)


@csrf_exempt
def uploadAdapter(request):
    """Uploader to save image"""
    path = os.path.join(settings.MEDIA_ROOT, "contents")

    try:
        uploadImg = request.FILES.get("upload")
        newImg = None

        if uploadImg:
            with Image.open(uploadImg.file.name) as image:
                imgId = shortuuid.ShortUUID().random(length=5)
                newImg = f"{imgId}_{uploadImg.name}"
                savePath = os.path.join(path, newImg)
                image.save(savePath, format=image.format)

        url = request.build_absolute_uri(f"{settings.MEDIA_URL}contents/{newImg}")
        return JsonResponse(data={"message": "success", "url": url}, status=200)

    except Exception as e:
        return JsonResponse(data={"error": "Internal error"}, status=500)


""" 
Utility functions 
Fucntions that do not handle view directly
"""


def pagination(request, posts):
    """Pagination in django"""
    page = request.GET.get("page", 1)

    paginator = Paginator(posts, 5)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return posts


def filterPosts(request, posts):
    """Filter post on get request"""
    tags = []
    queryPath = ""

    category = request.GET.get("category")
    if category:
        posts = posts.filter(category__name__icontains=category)
        tags.append({"query": "category", "value": category})
        queryPath += f"&category={category}"

    search = request.GET.get("search")
    if search:
        posts = posts.filter(
            Q(content__icontains=search)
            | Q(description__icontains=search)
            | Q(title__icontains=search)
            | Q(category__name__icontains=search)
        )
        tags.append({"query": "search", "value": f"'{search}'"})
        queryPath = (
            f"&search={search}" if not queryPath else queryPath + f"&search={search}"
        )

    print(queryPath)
    return posts, tags, queryPath


def getRelatedPost(post):
    """Get 6 posts that related to the post arg in terms of author or category"""
    authorRelatedPosts = Post.objects.filter(author=post.author).exclude(id=post.id)[:3]
    categoryRelatedPosts = Post.objects.filter(category=post.category).exclude(
        Q(id=post.id) | Q(author=post.author)
    )[:3]

    return {
        "author": authorRelatedPosts,
        "category": categoryRelatedPosts,
    }


def commentResponseData(newComment, request):
    """generate response data for new comment"""
    responseData = {}

    if newComment.commentor:
        commentor = newComment.commentor.email
        bloggerUrl = request.build_absolute_uri(
            reverse("bloggerHome", kwargs={"email": commentor})
        )
    else:
        commentor = "Guest"
        bloggerUrl = None

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
            "commentId": newComment.id,
            "commentor": commentor,
            "dateCreated": formatDate,
            "content": request.POST.get("content"),
            "bloggerUrl": bloggerUrl,
        }
    )
    return responseData


def categoryHandler(request):
    """Handle new category when create or edit a post"""
    name = request.POST.get("category")

    categories = Category.objects.filter(name__icontains=name)

    if not categories.exists() or name == "":
        newCategory = Category.objects.create(name=request.POST.get("new-category"))
        return newCategory

    return categories[0]


# print(request.resolver_match.view_name)
