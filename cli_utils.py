import os
import sys
import requests

URL='http://127.0.0.1:5000/'

# get requests - 19

def get_movies():
    r = requests.get(url = URL+'movies')
    data = r.json()
    return data

def get_specific_movie(query):
    r = requests.get(url = URL+'movies/'+query)
    data = r.json()
    return data

def search_movie_by_name(query):
    r = requests.get(url = URL+'movies/search/'+query)
    data = r.json()
    return data

def search_movie_by_review(query):
    r = requests.get(url = URL+'review/search/'+query)
    data = r.json()
    return data

def filter_movie_by_score(query):
    r = requests.get(url = URL+'scores/filter/'+query)
    data = r.json()
    return data

def search_movie_by_score(query):
    r = requests.get(url = URL+'scores/search/'+query)
    data = r.json()
    return data

def get_users():
    r = requests.get(url = URL+'users')
    data = r.json()
    return data

def find_review_by_movie_id(query):
    r = requests.get(url = URL+'review/'+query)
    data = r.json()
    return data

def find_score_by_movie_id(query):
    r = requests.get(url = URL+'scores/'+query)
    data = r.json()
    return data

def highest_scoring_movie():
    r = requests.get(url = URL+'scores/high')
    data = r.json()
    return data

def highest_scoring_movies(query):
    r = requests.get(url = URL+'scores/high/'+query)
    data = r.json()
    return data

def lowest_scoring_movies(query):
    r = requests.get(url = URL+'scores/low/'+query)
    data = r.json()
    return data

def search_by_genre(query):
    r = requests.get(url = URL+'genre/search/'+query)
    data = r.json()
    return data

def search_by_cast(query):
    r = requests.get(url = URL+'cast/search/'+query)
    data = r.json()
    return data

def filter_by_box_office_collection(query):
    r = requests.get(url = URL+'/money/filter/'+query)
    data = r.json()
    return data

def highest_grossing_movie():
    r = requests.get(url = URL+'/money/high')
    data = r.json()
    return data

def lowest_grossing_movie():
    r = requests.get(url = URL+'/money/low')
    data = r.json()
    return data

def highest_grossing_movies(query):
    r = requests.get(url = URL+'/money/highest/'+query)
    data = r.json()
    return data

# post requests - 3
# put requests - 3
# delete requests - 1


