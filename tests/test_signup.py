import json
import requests

from tests.base import BaseCase

class TestUserSignup(BaseCase):

    def test_successful_signup(self):
        # Given
        payload = json.dumps({
            "email": "nepal@gmail.com",
            "password": "jainepal"
        })

        # When
        response = requests.post('http://127.0.0.1:5000/signup/auth', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(str, type(response.json()['user_id']))
        self.assertEqual(200, response.status_code)

    def test_signup_with_non_existing_field(self):
        #Given
        payload = json.dumps({
            "username": "nepali95",
            "email": "nepal@gmail.com",
            "password": "jainepal"
        })

        #When
        response = requests.post('http://127.0.0.1:5000/signup/auth', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual('Request is missing required fields', response.json()['message'])
        self.assertEqual(400, response.status_code)

    def test_signup_without_email(self):
        #Given
        payload = json.dumps({
            "password": "jainepal",
        })

        #When
        response = requests.post('http://127.0.0.1:5000/signup/auth', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual('Something went wrong', response.json()['message'])
        self.assertEqual(500, response.status_code)

    def test_signup_without_password(self):
        #Given
        payload = json.dumps({
            "email": "nepal@gmail.com",
        })

        #When
        response = requests.post('http://127.0.0.1:5000/signup/auth', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual('Something went wrong', response.json()['message'])
        self.assertEqual(500, response.status_code)

    def test_creating_already_existing_user(self):
        #Given
        payload = json.dumps({
            "email": "nepal@gmail.com",
            "password": "jainepal"
        })
        response = requests.post('http://127.0.0.1:5000/signup/auth', headers={"Content-Type": "application/json"}, data=payload)

        # When
        response = requests.post('http://127.0.0.1:5000/signup/auth', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual('User with given email address already exists', response.json()['message'])
        self.assertEqual(400, response.status_code)