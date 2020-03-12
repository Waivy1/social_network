# from django.test import TestCase
from unittest import TestCase

from rest_framework.test import APIRequestFactory

from .views import UserSignUp, UserLogin


class UserLoginRegisterTestCase(TestCase):
    def test_sign_up(self):
        factory = APIRequestFactory()
        # simple sign up
        fake_request = factory.post('/sign_up', {'login': 'a',
                                                 'password': 'b'})
        # invalid input key: login
        fake_request2 = factory.post('/sign_up', {'logi': 'a',
                                                 'password': 'b'})
        # empty values
        fake_request4 = factory.post('/sign_up', {'login': '',
                                                 'password': ''})
        # > 50 characters
        fake_request5 = factory.post('/sign_up', {'login':
                                                      '1'*100,
                                                  'password': ''})
        json_response = UserSignUp().post(fake_request)
        json_response2 = UserSignUp().post(fake_request)
        json_response3 = UserSignUp().post(fake_request2)
        json_response4 = UserSignUp().post(fake_request4)
        json_response5 = UserSignUp().post(fake_request5)

        self.assertEquals(json_response.status_code, 200)
        self.assertEquals(json_response2.status_code, 400)
        self.assertEquals(json_response3.status_code, 400)
        self.assertEquals(json_response4.status_code, 400)
        self.assertEquals(json_response5.status_code, 400)

    def test_login(self):
        factory = APIRequestFactory()
        fake_request = factory.post('/login', {'login': 'a',
                                                 'password': 'b'})

        json_response = UserLogin().post(fake_request)
        self.assertEquals(json_response.status_code, 200)
