# from django.test import TestCase
from unittest import TestCase

from rest_framework.test import APIRequestFactory

from .views import UserSignUp, UserLogin, CreatePost


class UserLoginRegisterTestCase(TestCase):
    # def test_sign_up(self):
    #     factory = APIRequestFactory()
    #     # simple sign up
    #     fake_request = factory.post('/sign_up', {'login': 'a', 'password': 'b'})
    #     # json_response = UserSignUp().post(fake_request)
    #     # self.assertEquals(json_response.status_code, 200)
    #
    #     json_response2 = UserSignUp().post(fake_request)
    #     self.assertEquals(json_response2.status_code, 400)
    #
    #     # invalid input key: login
    #     fake_request2 = factory.post('/sign_up', {'logi': 'a11', 'password': 'b'})
    #     json_response3 = UserSignUp().post(fake_request2)
    #     self.assertEquals(json_response3.status_code, 400)
    #
    #     # empty values
    #     fake_request4 = factory.post('/sign_up', {'login': '', 'password': ''})
    #     json_response4 = UserSignUp().post(fake_request4)
    #     self.assertEquals(json_response4.status_code, 400)
    #
    #     # > 50 characters
    #     fake_request5 = factory.post('/sign_up', {'login': '1'*100, 'password': ''})
    #     json_response5 = UserSignUp().post(fake_request5)
    #     self.assertEquals(json_response5.status_code, 400)



    # def test_login(self):
    #     factory = APIRequestFactory()
    #     fake_request = factory.post('/login', {'login': 'a', 'password': 'b'})
    #
    #     json_response = UserLogin().post(fake_request)
    #     self.assertEquals(json_response.status_code, 200)
    #
    #     fake_request2 = factory.post('/login', {'logi': 'a11', 'password': 'b'})
    #     json_response3 = UserSignUp().post(fake_request2)
    #     self.assertEquals(json_response3.status_code, 400)
    #
    #     fake_request4 = factory.post('/login', {'login': '', 'password': ''})
    #     json_response4 = UserSignUp().post(fake_request4)
    #     self.assertEquals(json_response4.status_code, 400)
    #
    #     fake_request5 = factory.post('/login', {'login': '1'*100, 'password': ''})
    #     json_response5 = UserSignUp().post(fake_request5)
    #     self.assertEquals(json_response5.status_code, 400)


    def test_post(self):
        factory = APIRequestFactory()
        fake_request = factory.post('/create_post', {'text': 'agfyppyfuidh'})
        json_response = CreatePost().post(fake_request)
        self.assertEquals(json_response.status_code, 200)

        fake_request2 = factory.post('/create_post', {'text': ''})
        json_response2 = CreatePost().post(fake_request2)
        self.assertEquals(json_response2.status_code, 400)

        fake_request3 = factory.post('/create_post', {'': 'oeuidh'})
        json_response3 = CreatePost().post(fake_request3)
        self.assertEquals(json_response3.status_code, 400)