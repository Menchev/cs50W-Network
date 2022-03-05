import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User, Post, Follow
from .forms import NewPostForm


def index(request):
    # if the method is get
    if request.method == 'GET':

        # order the posts by descending order of timestamp
        posts = Post.objects.all().order_by("-timestamp")

        # implementing pagination feature
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "network/index.html", {
            'page_obj': page_obj,
            'NewPostForm': NewPostForm()
        })

    #  if the request method is PUT updating a post
    if request.method == 'PUT':
        data = json.loads(request.body)
        index = data.get('index', "")
        content = data.get('content', "")
        posts = Post.objects.all().order_by("-timestamp")
        posts[index].content = content
        posts[index].save()
        return HttpResponse(status=204)

    # if the method is POST (a use is posting)
    if request.method == 'POST':
        # populate the form with the info
        newPostForm = NewPostForm(request.POST)
        #validate the content
        if newPostForm.is_valid():
            content = newPostForm.cleaned_data["content"]
            Post.objects.create(user=request.user ,content=content)
            # reverse render the index view
            return HttpResponseRedirect(reverse('index'))

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

@login_required
@csrf_exempt
# profile page
def profile_view(request,user_id):

    # get the user
    userProfile = User.objects.get(pk=user_id)

    # check if the user is requesting its own profile page
    if request.user == userProfile:
        is_users_profile = True
    elif request.user != userProfile:
        is_users_profile = False

    # if the request is get - to view the profile page
    if request.method == 'GET':
        posts = Post.objects.filter(user=userProfile).order_by("-timestamp")
        if request.method == 'GET':
            return render(request, "network/profile.html", {
                'user': userProfile,
                'posts': posts
            })

    # if the method is POST - to get the follow info for the profile
    if request.method == 'POST':

        # check if the user is following the userProfile already
        try:
            Follow.objects.get(follower=request.user, followed=userProfile)
            is_follower = True
        except:
            is_follower = False

        # get the counts of following and follower
        followers = userProfile.followers.count()
        following = userProfile.following.count()
        
        # return the outcome
        return JsonResponse({
            "is_follower": is_follower, 
            "followers": followers, 
            "following": following,
            "is_users_profile": is_users_profile
            })

    # if a PUT request method is received (follow/unfollow btn clicked)
    if request.method == 'PUT':
        # check if the user is following the userProfile already
        try:
            Follow.objects.get(follower=request.user, followed=userProfile).delete()
            is_follower = False
        except:
            Follow.objects.create(follower=request.user, followed=userProfile)
            is_follower = True

        # get the counts of following and follower
        followers = userProfile.followers.count()
        following = userProfile.following.count()
        
        # return the outcome
        return JsonResponse({
            "is_follower": is_follower, 
            "followers": followers, 
            "following": following
            })

@login_required
# all posts view
def following_posts_view(request):
    # if request method is get
    if request.method == 'GET':

        # get all profiles that are being followed and put them in a variable
        following_users = request.user.following.all()

        # container for all posts made by profiles that are being followed
        posts = []

        # loop over each profile and get the user's posts. Afterwards, store them in a variable
        for followed_user in following_users:
            followed_user_posts = followed_user.followed.posts.all()
            try:
                # if there are multiple posts
                for post in followed_user_posts:
                    posts += post
            except:
                # if there are 1 or 0 posts made by this user
                posts += followed_user_posts
        
        # sort the posts in reverse chronological order
        posts.sort(key=lambda x: x.timestamp, reverse=True)

        # pass the acquired data to the html file
        return render(request, "network/following_posts.html", {
            'posts': posts
        })

@login_required
@csrf_exempt
def edit_post(request):
    if request.method != 'POST':
        return HttpResponse("incorred request method")

    data = json.loads(request.body)
    post_id = data.get("post_id", "")
    post = Post.objects.get(pk=post_id)
    post.content = data.get("content", "")
    post.save()
    return JsonResponse({"message": "post updated successfuly"}, status=204)