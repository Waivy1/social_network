from random import randint
from unittest import TestCase

from rest_framework.test import APIRequestFactory

from .. import models
from ..views import UserSignUp, UserLogin, CreatePost, LikePost, DislikePost


class UserSignUpTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_sign_up(self):
        fake_request = self.factory.post('/sign_up', {'login': 'a3', 'password': 'b'})
        json_response = UserSignUp().post(fake_request)
        self.assertEquals(json_response.status_code, 200)

        json_response2 = UserSignUp().post(fake_request)
        self.assertEquals(json_response2.status_code, 400)

    def test_wrong_value(self):
        fake_request2 = self.factory.post('/sign_up', {'logi': 'a11', 'password': 'b'})
        json_response3 = UserSignUp().post(fake_request2)
        self.assertEquals(json_response3.status_code, 400)

    def test_empty_value(self):
        fake_request4 = self.factory.post('/sign_up', {'login': '', 'password': ''})
        json_response4 = UserSignUp().post(fake_request4)
        self.assertEquals(json_response4.status_code, 400)

    def test_big_value(self):
        fake_request5 = self.factory.post('/sign_up', {'login': '1'*100, 'password': ''})
        json_response5 = UserSignUp().post(fake_request5)
        self.assertEquals(json_response5.status_code, 400)


class UserLoginTestCase(TestCase):
    def setUp(self) -> None:
        self._create_user()
        self.factory = APIRequestFactory()

    def _create_user(self):
        self.user_id = randint(1, 1337)
        models.User(id=self.user_id, login=self.user_id, password=1337).save()

    def test_login(self):
        fake_request = self.factory.post('/login', {'login': self.user_id, 'password': 1337})
        json_response = UserLogin().post(fake_request)
        self.assertEquals(json_response.status_code, 200)

    def test_wrong_value(self):
        fake_request2 = self.factory.post('/login', {'logi': 'a11', 'password': 'b'})
        json_response3 = UserLogin().post(fake_request2)
        self.assertEquals(json_response3.status_code, 400)

    def test_empty_value(self):
        fake_request4 = self.factory.post('/login', {'login': '', 'password': ''})
        json_response4 = UserLogin().post(fake_request4)
        self.assertEquals(json_response4.status_code, 400)

    def test_big_value(self):
        fake_request5 = self.factory.post('/login', {'login': '1'*100, 'password': ''})
        json_response5 = UserLogin().post(fake_request5)
        self.assertEquals(json_response5.status_code, 400)


class CreatePostTestCase(TestCase):
    def test_post(self):
        self.factory = APIRequestFactory()
        fake_request = self.factory.post('/create_post', {'text': 'agfyppyfuidh'})
        json_response = CreatePost().post(fake_request)
        self.assertEquals(json_response.status_code, 200)

    def empty_value(self):
        fake_request2 = self.factory.post('/create_post', {'text': ''})
        json_response2 = CreatePost().post(fake_request2)
        self.assertEquals(json_response2.status_code, 400)

    def wrong_value(self):
        fake_request3 = self.factory.post('/create_post', {'': 'oeuidh'})
        json_response3 = CreatePost().post(fake_request3)
        self.assertEquals(json_response3.status_code, 400)


class LikePostTestCase(TestCase):
    def setUp(self) -> None:
        self._create_user_post()
        self._create_disliked_post()

    def _create_user_post(self):
        self.user_id = randint(1, 1337)
        self.post_id = randint(1, 1337)

        models.User(id=self.user_id, login=self.user_id, password=1337).save()
        models.Post(id=self.post_id, text="1337").save()

    def _create_disliked_post(self):
        self.user_id_disliked = self.user_id + 10
        self.post_id_disliked = self.post_id + 10
        self.disliked_post = randint(1, 1337)

        user_obj = models.User(id=self.user_id_disliked, login=self.user_id_disliked, password=1337)
        user_obj.save()
        post_obj = models.Post(id=self.post_id_disliked, text="1337")
        post_obj.save()

        models.LikedPosts(id=self.disliked_post, post_id=post_obj, user_id=user_obj, is_liked=False).save()
        self.factory = APIRequestFactory()

    def test_successful_like(self):
        fake_request = self.factory.post('/like_post', {'post_id': self.post_id, 'user_id': self.user_id})
        json_response = LikePost().post(fake_request)
        self.assertEquals(json_response.status_code, 200)

    def test_user_does_not_exist(self):
        fake_request = self.factory.post('/like_post', {'post_id': self.post_id,
                                                        'user_id': self.user_id * randint(10, 100)})
        json_response = LikePost().post(fake_request)

        self.assertEquals(json_response.status_code, 400)
        self.assertEquals(json_response.content, b'{"message": "user or post don`t exist "}')

    def test_post_liked_again(self):
        fake_request = self.factory.post('/like_post', {'post_id': self.post_id_disliked,
                                                        'user_id': self.user_id_disliked})
        json_response = LikePost().post(fake_request)
        self.assertEquals(json_response.status_code, 200)

        liked_post = models.LikedPosts.objects.get(id=self.disliked_post)
        self.assertEquals(liked_post.is_liked, True)

    def test_empty_value(self):
        fake_request = self.factory.post('/like_post', {'post_id': '', 'user_id': self.user_id})
        json_response = LikePost().post(fake_request)
        self.assertEquals(json_response.status_code, 400)

    def test_w_value(self):
        fake_request = self.factory.post('/like_post', {'post_': self.post_id, 'user_id': self.user_id})
        json_response = LikePost().post(fake_request)
        self.assertEquals(json_response.status_code, 400)


class DislikePostTestCase(TestCase):
    def setUp(self) -> None:
        self._create_user_post()
        self._create_liked_post()

    def _create_user_post(self):
        self.user_id = randint(1, 1337)
        self.post_id = randint(1, 1337)

        models.User(id=self.user_id, login=self.user_id, password=1337).save()
        models.Post(id=self.post_id, text="1337").save()

    def _create_liked_post(self):
        self.user_id_liked = self.user_id + 10
        self.post_id_liked = self.post_id + 10
        self.disliked_post = randint(1, 1337)

        user_obj = models.User(id=self.user_id_liked, login=self.user_id_liked, password=1337)
        user_obj.save()
        post_obj = models.Post(id=self.post_id_liked, text="1337")
        post_obj.save()

        models.LikedPosts(id=self.disliked_post, post_id=post_obj, user_id=user_obj, is_liked=True).save()
        self.factory = APIRequestFactory()

    def test_successful_dislike(self):
        fake_request = self.factory.post('/dislike_post', {'post_id': self.post_id_liked,
                                                           'user_id': self.user_id_liked})
        json_response = DislikePost().post(fake_request)
        self.assertEquals(json_response.status_code, 200)

    def test_user_does_not_exist(self):
        fake_request = self.factory.post('/dislike_post', {'post_id': self.post_id,
                                                           'user_id': self.user_id * randint(10, 100)})
        json_response = DislikePost().post(fake_request)

        self.assertEquals(json_response.status_code, 400)
        self.assertEquals(json_response.content, b'{"message": "user or post don`t exist "}')

    def test_empty_value(self):
        fake_request = self.factory.post('/dislike_post', {'post_id': '', 'user_id': self.user_id})
        json_response = DislikePost().post(fake_request)
        self.assertEquals(json_response.status_code, 400)

    def test_w_value(self):
        fake_request = self.factory.post('/dislike_post', {'post_': self.post_id, 'user_id': self.user_id})
        json_response = DislikePost().post(fake_request)
        self.assertEquals(json_response.status_code, 400)

