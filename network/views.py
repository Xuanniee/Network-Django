from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, UserProfile
from .forms import NewPost, NewPostComment


def index(request):
    # POST Request - Submit Post
    if request.method == "POST":
        current_user = request.user
        # Post Button
        # Get Form Details
        user_post_content = request.POST["posting_area"]
        # Add the Post to a Post Object and Save
        user_post = Post(user=current_user, post_content=user_post_content)
        user_post.save()
        # Redirect to All Posts
        return HttpResponseRedirect(reverse("index"))
    
    # GET Request
    else:
        # Retrieve all the Posts that are available
        public_posts = Post.objects.all()

        # Translate into a List of Objects
        public_posts_list = []
        for object in public_posts:
            public_posts_list.append(object)

        # Give a List of Objects and the Number of Items per Page
        public_posts_paginator = Paginator(public_posts_list, 10)   # Show 10 per Page

        # Retrieve Page Number and Page Object
        page_number = request.GET.get('page')       # When User clicks on a Page Number
        page_obj = public_posts_paginator.get_page(page_number)

        # Post Content
        
        return render(request, "network/index.html", {
            "post_form": NewPost(),
            'page_obj': page_obj
        })


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

        # Create a User Profile for the User as well
        new_userprofile = UserProfile(user=user)
        new_userprofile.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profile(request, profile_id):
    # Get the Profile of the Requested User
    requested_profile = UserProfile.objects.filter(profile_id=profile_id)
    requested_user = requested_profile[0]
    requested_user = requested_user.user
    
    current_user = request.user
    #print(f"Current User: {current_user}; Requested User: {requested_user}")

    if request.method == "POST":
        # Get a Following List
        current_user_following_list = current_user.following_list

        # Check if User wants to Follow/Unfollow Requested User
        if request.POST.get("Follow-Button") == "Follow":
            # Add Requested User to my Following
            current_user_following_list.add(requested_user)

        elif request.POST.get("Unfollow-Button") == "Unfollow":
            # Remove Requested User
            current_user_following_list.remove(requested_user)

        # Redirect back to RU's Profile
        return HttpResponseRedirect(reverse("profile", args=(profile_id, )))    # Gotta make it a Tuple

    else:        
        # Retrieve all Personal Posts
        personal_posts = Post.objects.filter(user=requested_user)

        # Convert the Posts into a Paginator
        personal_posts_object_list = []
        for object in personal_posts:
            personal_posts_object_list.append(object)
        personal_posts_paginator = Paginator(personal_posts_object_list, 10)  # Object List, then Number of Items per Page

        # Retrieve Page Number
        personal_page_num = request.GET.get('page')

        # Retrieve Objects on Page
        personal_page_obj = personal_posts_paginator.get_page(personal_page_num)

        # Get Number of Followers and Following
        follower_num = requested_user.Followers.all().count()
        following_num = requested_user.following_list.all().count()

        return render(request, "network/profile.html", {
            "requested_profile": requested_profile,
            "follower_num": follower_num,
            "following_num": following_num,
            "requested_user": requested_user,
            'personal_page_obj': personal_page_obj
        })

# Posts from People we Followed
def following(request, user_id):
    current_user = request.user

    # Get the List of Users we are Following
    users_we_following = current_user.following_list.all()
    # Need to index the QuerySet to get the User Object
    try:
        users_we_following = users_we_following[0]
        # Get the List of Posts Objects from Users we are Following
        posts_from_following_list = Post.objects.filter(user=users_we_following)
    except IndexError:
        posts_from_following_list = []
    
    if (len(posts_from_following_list) == 0):
        following = False
    else:
        following = True

    return render(request, "network/following.html", {
        "following_posts": posts_from_following_list,
        "following": following
    })
    