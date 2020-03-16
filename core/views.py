from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from . import models
from .helpers import input_validate, ValidationError, EmptyValueError


@method_decorator(csrf_exempt, name='dispatch')
class UserSignUp(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            input_login, input_password = input_validate(request, ['login', 'password'])

        except ValidationError as e:
            return JsonResponse({'message': f'validation error in {e.args[0]}'}, status=400)

        except EmptyValueError as e:
            return JsonResponse({'message': 'value is empty'}, status=400)

        try:
            new_user = models.User(login=input_login, password=input_password)
            new_user.save()

        # IntegrityError повторна реєстрація, юнік констрейн (аргемент в бд)
        except IntegrityError as e:
            return JsonResponse({'message': f'login \'{input_login}\' already '
                                            f'exist'}, status=400)

        return JsonResponse({'message': 'created new account'})


@method_decorator(csrf_exempt, name='dispatch')
class UserLogin(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            input_login, input_password = input_validate(request, ['login', 'password'])

        except ValidationError as e:
            return JsonResponse({'message': f'validation error in {e.args[0]}'}, status=400)

        except EmptyValueError as e:
            return JsonResponse({'message': 'value is empty'}, status=400)

        try:
            models.User.objects.get(login=input_login, password=input_password)

        except models.User.DoesNotExist as e:
            print('no User')
            return JsonResponse({'message': 'wrong password or login'}, status=400)

        return JsonResponse({'message': 'successful login'})


@method_decorator(csrf_exempt, name='dispatch')
class CreatePost(APIView):
    def post(self, request):
        try:
            input_text = input_validate(request, ['text'])

        except ValidationError as e:
            return JsonResponse({'message': f'validation error in {e.args[0]}'}, status=400)

        except EmptyValueError as e:
            return JsonResponse({'message': 'value is empty'}, status=400)


        post = models.Post(text=input_text)
        post.save()

        return JsonResponse({'message': f'you created a post {input_text}'})


@method_decorator(csrf_exempt, name='dispatch')
class LikePost(APIView):
    def post(self, request):
        try:
            input_post_id, input_user_id = input_validate(request, ['post_id', 'user_id'])

        except ValidationError as e:
            return JsonResponse({'message': f'validation error in {e.args[0]}'}, status=400)

        except EmptyValueError as e:
            return JsonResponse({'message': 'value is empty'}, status=400)

        try:
            user_obj = models.User.objects.get(id=input_user_id)
            post_obj = models.Post.objects.get(id=input_post_id)

        except ObjectDoesNotExist as e:
            return JsonResponse({'message': 'user or post don`t exist '}, status=400)

        try:
            liked_posts_obj = models.LikedPosts.objects.get(post_id=input_post_id, user_id=input_user_id)

        except models.LikedPosts.DoesNotExist as e:
            liked_post = models.LikedPosts(post_id=post_obj, user_id=user_obj)
            liked_post.save()

            return JsonResponse({'message': f'user {user_obj.login} liked post {post_obj.text}, the post has '
                                            f'{liked_post.get_likes()} '
                                            f'likes'})

        else:
            liked_posts_obj.is_liked = True
            liked_posts_obj.save()

            l = liked_posts_obj.get_likes()
            return JsonResponse({'message': f'user {user_obj.login} liked post {post_obj.text}, the post has {l} '
                                            f'likes'})


@method_decorator(csrf_exempt, name='dispatch')
class DislikePost(APIView):
    def post(self, request):
        try:
            input_post_id, input_user_id = input_validate(request, ['post_id', 'user_id'])

        except ValidationError as e:
            return JsonResponse({'message': f'validation error in {e.args[0]}'}, status=400)

        except EmptyValueError as e:
            return JsonResponse({'message': 'value is empty'}, status=400)


        try:
            user_obj = models.User.objects.get(id=input_user_id)
            post_obj = models.Post.objects.get(id=input_post_id)
        except ObjectDoesNotExist as e:
            return JsonResponse({'message': 'user or post don`t exist '}, status=400)

        liked_posts_obj = models.LikedPosts.objects.get(post_id=input_post_id, user_id=input_user_id)
        liked_posts_obj.is_liked = False
        liked_posts_obj.save()

        return JsonResponse({'message': f'user {user_obj.login} disliked post {post_obj.text}, the post has '
                                        f'{liked_posts_obj.get_likes()} '
                                        f'likes'})
