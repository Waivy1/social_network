from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
import random
import datetime
from . import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .helpers import check_login_password_input


@method_decorator(csrf_exempt, name='dispatch')
class UserSignUp(View):
    def post(self, request):
        # todo: нагадати про дублювання коли написання юніт тестів
        is_valid, login, password = check_login_password_input(request)
        if not is_valid:
            return JsonResponse({'message': 'wrong input data'}, status=400)

        try:
            new_user = models.User(login=login, password=password)
            new_user.save()

        # IntegrityError повторна реєстрація, юнік констрейн (аргемент в бд)
        except IntegrityError as e:
            return JsonResponse({'message': f'login \'{login}\' already '
                                            f'exist'}, status=400)

        return JsonResponse({'message': 'created new account'})


@method_decorator(csrf_exempt, name='dispatch')
class UserLogin(View):
    def post(self, request):
        try:
            input_login = request.POST['login']
            input_password = request.POST['password']

        except KeyError as e:
            return JsonResponse({'message': 'wrong input data'}, status=400)

        try:
            user = models.User.objects.get(login=input_login,
                                           password=input_password)

        except models.User.DoesNotExist as e:
            print('no User')
            return JsonResponse({'message': 'wrong password or login'},
                                status=404)

        return JsonResponse({'message': 'successful login'})


@method_decorator(csrf_exempt, name='dispatch')
class CreatePost(View):
    def post(self, request):
        input_text = request.POST['text']

        post = models.Post(text=input_text)
        post.save()

        return JsonResponse({'message': f'you created a post {input_text}'})


@method_decorator(csrf_exempt, name='dispatch')
class LikePost(View):
    def post(self, request):
        input_post_id = request.POST['post_id']
        input_user_id = request.POST['user_id']

        user_obj = models.User.objects.get(id=input_user_id)
        post_obj = models.Post.objects.get(id=input_post_id)

        try:
            liked_posts_obj = models.LikedPosts.objects.get(post_id=input_post_id, user_id=input_user_id)

        except models.LikedPosts.DoesNotExist as e:
            liked_post = models.LikedPosts(post_id=post_obj, user_id=user_obj)
            liked_post.save()

            # leng = len(models.LikedPosts.objects.filter(post_id=post_obj, is_liked=True))  # -> []
            leng = liked_post.get_likes()
            return JsonResponse({'message': f'user {user_obj.login} liked post {post_obj.text}, the post has {leng} '
                                            f'likes'})

        else:
            liked_posts_obj.is_liked = True
            liked_posts_obj.save()

            leng = len(models.LikedPosts.objects.filter(post_id=post_obj, is_liked=True))  # -> []
            return JsonResponse({'message': f'user {user_obj.login} liked post {post_obj.text}, the post has {leng} '
                                            f'likes'})


@method_decorator(csrf_exempt, name='dispatch')
class DislikePost(View):
    def post(self, request):
        input_post_id = request.POST['post_id']
        input_user_id = request.POST['user_id']

        user_obj = models.User.objects.get(id=input_user_id)
        post_obj = models.Post.objects.get(id=input_post_id)

        liked_posts_obj = models.LikedPosts.objects.get(post_id=input_post_id, user_id=input_user_id)
        liked_posts_obj.is_liked = False
        liked_posts_obj.save()

        leng = len(models.LikedPosts.objects.filter(post_id=post_obj, is_liked=True))

        return JsonResponse({'message': f'user {user_obj.login} disliked post {post_obj.text}, the post has {leng} '
                                        f'likes'})









