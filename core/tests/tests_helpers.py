from random import randint
from unittest import TestCase

from rest_framework.test import APIRequestFactory

from ..helpers import input_validate, ValidationError, EmptyValueError
from ..views import UserSignUp


class InputValidateTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_success(self):
        expected_login = 'a'
        expected_password = 'b'
        fake_request = self.factory.post('', {'login': expected_login,
                                              'password': expected_password})

        login, password = input_validate(fake_request, ['login', 'password'])

        self.assertEquals(login, expected_login)
        self.assertEquals(password, expected_password)

    def test_wrong_keys(self):
        expected_login = 'a'
        expected_password = 'b'
        fake_request = self.factory.post('', {'wrong_key': expected_login,
                                              'password': expected_password})
        try:
            login, password = input_validate(fake_request, ['login', 'password'])
        except ValidationError as e:
            self.assertEquals('login', e.args[0])

    def test_empty_values(self):
        expected_login = 'a'
        expected_password = 'b'
        fake_request = self.factory.post('', {'login': '',
                                              'password': ''})
        try:
            login, password = input_validate(fake_request, ['login', 'password'])
        except EmptyValueError as e:
            self.assertEquals(tuple(), e.args)









