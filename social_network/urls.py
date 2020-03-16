from django.urls import path
from core import views

from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('sign_up', views.UserSignUp.as_view(), name='sign_up'),
    path('login', views.UserLogin.as_view(), name='login'),
    path('create_post', views.CreatePost.as_view(), name='create_post'),
    path('like_post', views.LikePost.as_view(), name='like_post'),
    path('dislike_post', views.DislikePost.as_view(), name='dislike_post'),

    ]
