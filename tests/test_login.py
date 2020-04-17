import json
import requests

from tests.base import BaseCase

class TestUserLogin(BaseCase):

    def test_login_success(self):
        # Given
        email = "nepal@gmail.com"
        password = "jainepal"
        payload = json.dumps({
            "email": email,
            "password": password
        })
        response = requests.post('http://127.0.0.1:5000/signup/auth', headers={"Content-Type": "application/json"}, data=payload)
        # When
        response = requests.post('http://127.0.0.1:5000/login/auth', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(str, type(response.json()['token']))
        self.assertEqual(200, response.status_code)

    def test_login_with_invalid_email(self):
        # Given
        email = "nepal@gmaili.com"
        password = "jainepal"
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post('http://127.0.0.1:5000/signup/auth', headers={"Content-Type": "application/json"}, data=json.dumps(payload))

        # When
        payload['email'] = "nepali@gmail.com"
        response = requests.post('http://127.0.0.1:5000/login/auth', headers={"Content-Type": "application/json"}, data=json.dumps(payload))

        # Then
        self.assertEqual("Invalid email or password", response.json()['message'])
        self.assertEqual(401, response.status_code)

    def test_login_with_invalid_password(self):
        # Given
        email = "nepal@gmail.com"
        password = "jainepali"
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post('http://127.0.0.1:5000/signup/auth', headers={"Content-Type": "application/json"}, data=json.dumps(payload))

        # When
        payload['password'] = "jainepal"
        response = requests.post('http://127.0.0.1:5000/login/auth', headers={"Content-Type": "application/json"}, data=json.dumps(payload))

        # Then
        self.assertEqual("Invalid email or password", response.json()['message'])
        self.assertEqual(401, response.status_code)