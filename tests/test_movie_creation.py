import json
import requests

from tests.base import BaseCase

class TestMovieCreation(BaseCase):

    def test_movie_creation(self):
        # Given
        email = "nepal@gmail.com"
        password = "jainepal"
        user_payload = json.dumps({
            "email": email,
            "password": password
        })

        requests.post('http://127.0.0.1:5000/signup/auth', headers={"Content-Type": "application/json"}, data=user_payload)
        response = requests.post('http://127.0.0.1:5000/login/auth', headers={"Content-Type": "application/json"}, data=user_payload)
        login_token = response.json()['token']

        movie_payload = {
            "name": "Star Wars: The Rise of Skywalker",
            "casts": ["Daisy Ridley", "Adam Driver"],
            "genres": ["Fantasy", "Sci-fi"],
            "reviews": ["this is good"]
        }
        # When
        response = requests.post('http://127.0.0.1:5000/movies',
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {login_token}"},
            data=json.dumps(movie_payload))

        # Then
        self.assertEqual(str, type(response.json()['id']))
        self.assertEqual(200, response.status_code)
        