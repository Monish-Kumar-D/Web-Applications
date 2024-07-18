from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Exists, OuterRef
from django.core.paginator import Paginator

from .models import User, Post, Follow, Like


# def index(request):
#     posts = Post.objects.order_by("-id")
#     return render(request, "network/index.html", {
#         "posts":posts
#     })

def index(request):
    user = request.user
    if not user.is_authenticated:
        total_posts = Post.objects.order_by("-id")
        paginator = Paginator(total_posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        posts = paginator.get_page(page_number)
        return render(request, "network/index.html", {"posts": posts, "page_obj" : page_obj})

    else:
        total_posts = Post.objects.annotate(
            liked_by_user=Exists(
                Like.objects.filter(post_id=OuterRef('pk'), user=request.user)
            )
        ).order_by("-id")
        paginator = Paginator(total_posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        posts = paginator.get_page(page_number)
        return render(request, "network/index.html", {"posts": posts, "page_obj" : page_obj})


def following_posts(request):
    user = request.user
    # Get the list of users that the current user follows
    followers = Follow.objects.filter(follower=user).values_list('user_id', flat=True)
    
    # Get the posts of the people that the current user follows in reverse chronological order
    total_posts = Post.objects.filter(username__id__in=followers).annotate(
        liked_by_user=Exists(
            Like.objects.filter(post_id=OuterRef('pk'), user=user)
        )
    ).order_by('-timestamp')
    paginator = Paginator(total_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    posts1 = paginator.get_page(page_number)
    return render(request, "network/followers.html", {"posts1": posts1, "poge_obj" : page_obj})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url='login/')
def newpost(request):
    #if the method is post
    if request.method == "POST":
        #obtain the user details and the content of the post was made
        username = request.user
        content = request.POST['content']

        #create a model instance and save the instance with this content
        new_post = Post(username=username, content=content)
        new_post.save()
        return HttpResponseRedirect(reverse('index'))
    elif request.method == "GET":
        try:       
            return render(request, 'network/newpost.html')
        except:
            HttpResponseRedirect('login')


@login_required
def profile(request, profile_id):
    user = get_object_or_404(User, pk=profile_id)
    total_posts = Post.objects.filter(username=user).order_by('-timestamp')
    paginator = Paginator(total_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    posts = paginator.get_page(page_number)
    followers_count = Follow.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()

    is_following = Follow.objects.filter(user=user, follower=request.user).exists()

    return render(request, "network/profile.html", {
        "posts": posts,
        "page_obj" : page_obj,
        "profile_user": user,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following
    })


@csrf_exempt
@login_required
def follow(request, profile_id):
    user_to_follow = get_object_or_404(User, pk=profile_id)
    if request.method == "POST":
        Follow.objects.get_or_create(user=user_to_follow, follower=request.user)
        return JsonResponse({"message": "Followed"}, status=201)
    return HttpResponseBadRequest()


@csrf_exempt
@login_required
def unfollow(request, profile_id):
    user_to_unfollow = get_object_or_404(User, pk=profile_id)
    if request.method == "POST":
        Follow.objects.filter(user=user_to_unfollow, follower=request.user).delete()
        return JsonResponse({"message": "Unfollowed"}, status=201)
    return HttpResponseBadRequest()
       

# @csrf_exempt
# @login_required
# def edit(request,edit_id):
#     if request.method == "POST":
#         content = request.POST.get("content")
#         Post.objects.filter(pk=edit_id).update(content = content)

        
#         return HttpResponseRedirect(reverse('index'))
#     else:
#         content = Post.objects.filter(pk=edit_id)
#         for cont in content:
#             if request.user == cont.username:
#                 return render(request,"network/edit.html", {
#                     "content" : content
#                 })
#             else:
#                 return HttpResponse("you're not the user")


@csrf_exempt
@login_required
def edit(request, edit_id):
    if request.method == "POST":
        content = request.POST.get("content")
        post = get_object_or_404(Post, pk=edit_id)
        
        if request.user == post.username:
            post.content = content
            post.save()
            return JsonResponse({"message": "Post updated successfully", "content": content}, status=200)
        else:
            return JsonResponse({"error": "You're not authorized to edit this post"}, status=403)
    else:
        post = get_object_or_404(Post, pk=edit_id)
        if request.user == post.user:
            return JsonResponse({"content": post.content}, status=200)
        else:
            return JsonResponse({"error": "You're not authorized to edit this post"}, status=403)
        

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return JsonResponse({'liked': liked, 'like_count': post.likes.count()})