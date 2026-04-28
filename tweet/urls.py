from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.tweet_list, name='tweet_list'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('edit/<int:tweet_id>/', views.tweet_edit, name='tweet_edit'),
    path('delete/<int:tweet_id>/', views.tweet_delete, name='tweet_delete'),

    path('register/', views.register, name='register'),  # ✅ THIS LINE IS MUST
    path('like/<int:tweet_id>/', views.like_tweet, name='like_tweet'),
    path('profile/<str:username>/', views.profile, name='profile'),
]