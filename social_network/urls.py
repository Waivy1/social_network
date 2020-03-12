from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('sign_up', views.UserSignUp.as_view(), name='sign_up'),
    path('login', views.UserLogin.as_view(), name='login'),
    path('create_post', views.CreatePost.as_view(), name='create_post'),
    path('like_post', views.LikePost.as_view(), name='like_post'),
    path('dislike_post', views.DislikePost.as_view(), name='dislike_post'),

    ]
