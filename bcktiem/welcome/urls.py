from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter





urlpatterns = [
    path('', views.welcome),
    path('signin/', views.signin, name='signin'),
    path('login/', LoginView.as_view(template_name='log-in.html'), name='login'),
    path('forgot_password/', views.forgot_password, name = 'forgot_password'),
    path('feed/', views.feed, name='feed'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.my_profile, name='my-profile'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/change-picture/', views.change_profile_picture, name='change_profile_picture'),
     path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('profile/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('profile/<str:username>/followers/', views.followers_list, name='followers'),
    path('profile/<str:username>/following/', views.following_list, name='following'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('post/<int:post_id>/save/', views.save_post, name='save-post'),
    #path('post/<int:post_id>/unsave/', views.unsave_post, name='unsave-post'),
    #path('post/<int:post_id>/delete/', views.delete_post, name='delete-post'),
    path('upload/', views.upload_post, name="upload_post"),
    #path('videos/', views.list_videos, name='list_videos'),
    path('notifications/', views.notifications, name='notifications'),
    path('friends/', views.friends, name='friends'),
    #path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
