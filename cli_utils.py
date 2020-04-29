import os
import sys
import requests

URL='http://127.0.0.1:5000/'

# get requests - 19

def get_movies():
    r = requests.get(url = URL+'movies')
    response = r.json()
    return response

def get_specific_movie(query):
    r = requests.get(url = URL+'movies/'+query)
    response = r.json()
    return response

def search_movie_by_name(query):
    r = requests.get(url = URL+'movies/search/'+query)
    response = r.json()
    return response

def search_movie_by_review(query):
    r = requests.get(url = URL+'review/search/'+query)
    response = r.json()
    return response

def filter_movie_by_score(query):
    r = requests.get(url = URL+'scores/filter/'+query)
    response = r.json()
    return response

def search_movie_by_score(query):
    r = requests.get(url = URL+'scores/search/'+query)
    response = r.json()
    return response

def get_users():
    r = requests.get(url = URL+'users/all')
    response = r.json()
    return response

def find_review_by_movie_id(query):
    r = requests.get(url = URL+'review/'+query)
    response = r.json()
    return response

def find_score_by_movie_id(query):
    r = requests.get(url = URL+'scores/'+query)
    response = r.json()
    return response

def highest_scoring_movie():
    r = requests.get(url = URL+'scores/high')
    response = r.json()
    return response

def highest_scoring_movies(query):
    r = requests.get(url = URL+'scores/high/'+query)
    response = r.json()
    return response

def lowest_scoring_movies(query):
    r = requests.get(url = URL+'scores/low/'+query)
    response = r.json()
    return response

def search_by_genre(query):
    r = requests.get(url = URL+'genre/search/'+query)
    response = r.json()
    return response

def search_by_cast(query):
    r = requests.get(url = URL+'cast/search/'+query)
    response = r.json()
    return response

def filter_by_box_office_collection(query):
    r = requests.get(url = URL+'/money/filter/'+query)
    response = r.json()
    return response

def highest_grossing_movie():
    r = requests.get(url = URL+'/money/high')
    response = r.json()
    return response

def lowest_grossing_movie():
    r = requests.get(url = URL+'/money/low')
    response = r.json()
    return response

def highest_grossing_movies(query):
    r = requests.get(url = URL+'/money/highest/'+query)
    response = r.json()
    return response

# post requests - 3

def add_movie(name, cast, genres, reviews, all_scores, box_office):
    data = {
        'name': name,
        'casts': cast,
        'genres': genres,
        'reviews': reviews,
        'all_scores': all_scores,
        'box_office': box_office
    }
    r = requests.post(url = URL+'/movies', response = data)
    response = r.json()
    return response

def signup(email, password):
    data = {
        'email': email,
        'password': password
    }
    r = requests.post(url = URL+'/signup/auth', response = data)
    response = r.json()
    return response

def login(email, password):
    data = {
        'email': email,
        'password': password
    }
    r = requests.post(url = URL+'/movies', response = data)
    response = r.json()
    return response

# put requests - 3
# delete requests - 1

def delete_movie(query):
    r = requests.get(url = URL+'/movies/'+query)
    status_code = r.status_code
    return status_code


