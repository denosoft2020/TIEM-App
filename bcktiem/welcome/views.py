from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Profile, Post
from .forms import ProfileUpdateForm, PostForm, ProfilePictureForm
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser





# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')


def signin(request):
    if request.method == "POST":
        username = request.POST["username"].strip()
        email = request.POST["email"].strip()
        password = request.POST["password"].strip()
        confirmPassword = request.POST["confirmPassword"].strip()

        if password != confirmPassword:
            messages.error(request, "Passwords do not match!")
            return redirect("signin")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("signin")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("signin")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        login(request, user)  # Log the user in after signing up
        messages.success(request, "Account created successfully!")
        return redirect("profile", username=username)  # Redirect to homepage

    return render(request, "sign-in.html")


@login_required
def home(request):
    return render(request, 'home.html')

def forgot_password(request):
    return render(request, 'forgot-password.html')

def feed(request):
    posts = Post.objects.all().order_by("-created_at")  # Show latest posts first
    print(posts)
    return render(request, "feed.html", {"posts": posts})
   

@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)
    if not profile.profile_picture:
        profile.profile_picture = 'profile_pictures/default.png'
        profile.save()
    
    
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)
    
    # Check if the current user is following this profile
    is_following = False
    if request.user.is_authenticated and request.user != user:
        is_following = request.user.profile.following.filter(pk=profile.pk).exists()
    
    # Get user posts
    posts = Post.objects.filter(user=user).order_by('-created_at')
    posts_count = posts.count()
    
    # Separate videos from images
    videos = posts.filter(video__isnull=False)
    images = posts.filter(image__isnull=False)
    
    # Get saved posts if viewing own profile
    saved_posts = []
    if request.user == user:
        saved_posts = request.user.saved_posts.all()
    
    context = {
        'user': user,
        'profile': profile,
        'posts_count': Post.objects.filter(user=user).count(),
        'followers_count': profile.followers.count(),
        'following_count': profile.following.count(),
        'likes_count': sum(post.likes.count() for post in Post.objects.filter(user=user)),
        'posts': Post.objects.filter(user=user).order_by('-created_at')[:9],
        'pinned_posts': Post.objects.filter(user=user, is_pinned=True),
    }
    
    return render(request, 'profile.html', context)

@login_required
@require_POST
def save_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.saved_by.filter(id=request.user.id).exists():
        post.saved_by.remove(request.user)
        saved = False
    else:
        post.saved_by.add(request.user)
        saved = True
    return JsonResponse({'saved': saved, 'count': post.saved_by.count()})



@login_required
@require_POST
def follow_user(request, username):
    if request.method == 'POST':
        user_to_follow = get_object_or_404(User, username=username)
        profile_to_follow = user_to_follow.profile
        current_profile = request.user.profile

        
        if request.user == user_to_follow:
            return JsonResponse({'error': 'You cannot follow yourself'}, status=400)
        
        profile_to_follow = user_to_follow.profile
        current_user_profile = request.user.profile
        
        data = json.loads(request.body)
        action = data.get('action', 'follow')
        
        if action == 'follow':
            current_user_profile.following.add(profile_to_follow)
        else:
            current_user_profile.following.remove(profile_to_follow)
        
        # Update followers count
        profile_to_follow.followers_count = profile_to_follow.followers.count()
        profile_to_follow.save()
        
        return JsonResponse({
            'status': 'success',
            'action': action,
            'followers_count': profile_to_follow.followers_count
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def change_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfilePictureForm(instance=request.user.profile)
    
    return render(request, 'change_picture.html', {'form': form})

@login_required
def followers_list(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    followers = profile.followers.all()
    return render(request, 'followers.html', {
        'profile': profile,
        'followers': followers,
        'current_tab': 'followers'
    })

@login_required
def following_list(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    following = profile.following.all()
    return render(request, 'following.html', {
        'profile': profile,
        'following': following,
        'current_tab': 'following'
    })

@login_required
def my_profile(request):
    # Redirect to the profile view with the current user's username
    return redirect('profile', username=request.user.username)
    
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'edit_profile.html', {'form': form})

    
@login_required
def upload_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.filter = request.POST.get("filter", "")  # Save selected filter
            post.duration = request.POST.get("duration", 15)  # Save duration
            post.save()
            return JsonResponse({"success": True, "message": "Post uploaded successfully!"})
        else:
            return JsonResponse({"success": False, "message": "Invalid form data"}, status=400)
    return render(request, "upload.html", {"form": PostForm()})



def notifications(request):
    return render(request, 'notifications.html')

def friends(request):
    return render(request, 'freinds.html')