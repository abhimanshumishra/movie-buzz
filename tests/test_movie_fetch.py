import unittest
import json
import requests

from tests.base import BaseCase

class TestGetMovies(BaseCase):

    def test_empty_response(self):
        response = requests.get('http://127.0.0.1:5000/movies')
        self.assertListEqual(response.json(), [])
        self.assertEqual(response.status_code, 200)

    def test_movie_response(self):
        # Given
        email = "nepal@gmail.com"
        password = "jainepal"
        user_payload = json.dumps({
            "email": email,
            "password": password
        })

        response = requests.post('http://127.0.0.1:5000/signup/auth', headers={"Content-Type": "application/json"}, data=user_payload)
        user_id = response.json()['user_id']
        response = requests.post('http://127.0.0.1:5000/login/auth', headers={"Content-Type": "application/json"}, data=user_payload)
        login_token = response.json()['token']

        movie_payload = {
            "name": "Star Wars: The Rise of Skywalker",
            "casts": ["Daisy Ridley", "Adam Driver"],
            "genres": ["Fantasy", "Sci-fi"],
            "reviews": ["This is good"]
        }
        response = requests.post('http://127.0.0.1:5000/movies',
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {login_token}"},
            data=json.dumps(movie_payload))

        # When
        response = requests.get('http://127.0.0.1:5000/movies')
        added_movie = response.json()[0]

        # Then
        self.assertEqual(movie_payload['name'], added_movie['name'])
        self.assertEqual(movie_payload['casts'], added_movie['casts'])
        self.assertEqual(movie_payload['genres'], added_movie['genres'])
        self.assertEqual(200, response.status_code)