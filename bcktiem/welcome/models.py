from django.shortcuts import render, redirect
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from rest_framework import serializers, viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.files.storage import default_storage
import os
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
#from .serializers import VideoSerializer



def user_profile_picture_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/profile_pictures/user_<id>/<filename>
    return f'profile_pictures/user_{instance.user.id}/{filename}'

def cover_photo_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/cover_photos/user_<id>/<filename>
    return f'cover_photos/user_{instance.user.id}/{filename}'

#model to the profile page
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    cover_photo = models.ImageField(upload_to='profiles/covers/', blank=True, null=True)
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    profile_picture = models.ImageField(
        upload_to=user_profile_picture_path,  # Use the defined function
        default='profile_pictures/default.jpg'
    )
    followers = models.ManyToManyField(
        'self',
        related_name='following',
        symmetrical=False,
        blank=True
    )

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

    cover_photo = models.ImageField(
        upload_to=cover_photo_path,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Model to store uploaded files (both images and videos)
# Django Model

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Who posted it
    caption = models.TextField(blank=True)  # Optional caption
    video = models.FileField(upload_to="uploads/videos/", blank=True, null=True)  # Video uploads
    image = models.ImageField(upload_to="uploads/images/", blank=True, null=True)  # Image uploads
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp
    saved_by = models.ManyToManyField(User, related_name='saved_posts', blank=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    is_pinned = models.BooleanField(default=False)

    @property
    def like_count(self):
        return self.likes.count()


    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at}"

def user_profile_picture_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/profile_pictures/user_<id>/<filename>
    return f'profile_pictures/user_{instance.user.id}/{filename}'


def cover_photo_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/cover_photos/user_<id>/<filename>
    return f'cover_photos/user_{instance.user.id}/{filename}'
