from flask import Flask, request, Response, jsonify, render_template
from database.models import Movie, User
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from database.db import initialize_db
from flask_bcrypt import Bcrypt
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError

import config
import os
import datetime

app = Flask(__name__)
app.config.from_pyfile('config.py')
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

db = initialize_db(app)

@app.route('/', methods=['GET'])
def hello():
    return 'Jai Nepal'

# signup related routes

@app.route('/signup/auth', methods=['POST'])
def signup():
    try:
        body = request.get_json(force=True)
        user = User(**body)
        user.hash_password()
        user.save()
        index = user.id
        return {'user_id': str(index)}, 200
    except FieldDoesNotExist:
        return {'message': "Request is missing required fields"}, 400
    except NotUniqueError:
        return {'message': "User with given email address already exists"}, 400
    except Exception as e:
        return {'message': "Something went wrong"}, 500

# login related routes

@app.route('/login/auth', methods=['POST'])
def login():
    try:
        body = request.get_json(force=True)
        user = User.objects.get(email=body.get('email'))
        authorized = user.check_password(body.get('password'))
        if not authorized:
            return {'message': "Invalid email or password"}, 401
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return {'token': access_token}, 200
    except DoesNotExist:
        return {'message': "Invalid email or password"}, 401
    except Exception as e:
        return {'message': "Something went wrong"}, 500

@app.route('/users/all', methods=['GET'])
def get_users():
    users = User.objects().to_json()
    return Response(users, mimetype="application/json", status=200)

# movie related routes

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.objects().to_json()
    return Response(movies, mimetype="application/json", status=200)

# search movie by index - one index corresponds only to one movie
@app.route('/movies/<index>', methods=['GET'])
def get_movie(index):
    try:
        movie = Movie.objects.get(id=index).to_json()
        return Response(movie, mimetype="application/json", status=200)
    except DoesNotExist:
        return {'message': "Movie with given id doesn't exist"}, 404
    except Exception as e:
        return {'message': "Something went wrong"}, 500

# add new movie
@jwt_required
@app.route('/movies', methods=['POST'])
def add_movie():
    try:
        body = request.get_json(force=True)
        movie = Movie(**body).save()
        idx = movie.id
        return {'id': str(idx)}, 200
    except InvalidQueryError:
        return {'message': "Request is missing required fields"}, 400
    except NotUniqueError:
        return {'message': "Movie with given name already exists"}, 400
    except Exception as e:
        return {'message': "Something went wrong"}, 500

# update movie details
@jwt_required
@app.route('/movies/<index>', methods=['PUT'])
def update_movie(index):
    try:
        body = request.get_json(force=True)
        Movie.objects.get(id=index).update(**body)
        return '', 200
    except InvalidQueryError:
        return {'message': "Request is missing required fields"}, 400
    except DoesNotExist:
        return {'message': "Updating movie added by others is forbidden"}, 400
    except Exception as e:
        return {'message': "Something went wrong"}, 500

@jwt_required
@app.route('/movies/<index>', methods=['DELETE'])
def delete_movie(index):
    try:
        Movie.objects.get(id=index).delete()
        return '', 200
    except DoesNotExist:
        return {'message': "Deleting movie added by others is forbidden"}, 400
    except Exception as e:
        return {'message': "Something went wrong"}, 500

@app.route('/movies/search/<query>', methods=['GET'])
def search_by_name(query):
    movies = Movie.objects()
    results = []
    for movie in movies:
        if query in movie.name.lower():
            results.append(movie)
    return {'results': results}, 200

# review related routes

# get all reviews of a movie using movie ID
@jwt_required
@app.route('/review/<index>', methods=['GET'])
def get_reviews(index):
    try:
        movie = Movie.objects.get(id=index)
        movie_reviews = movie['reviews']
        movie_reviews = list(movie_reviews)
        return {'reviews': movie_reviews}, 200 
    except InvalidQueryError:
        return {'message': "Request is missing required fields"}, 400
    except DoesNotExist:
        return {'message': "Updating movie added by others is forbidden"}, 400
    except Exception as e:
        return {'message': "Something went wrong"}, 500

# add new movie review
@jwt_required
@app.route('/review/<index>', methods=['PUT'])
def update_review(index):
    try:
        body = request.get_json(force=True)
        movie_reviews = Movie.objects.get(id=index)['reviews']
        movie_reviews = list(movie_reviews)
        movie_reviews.append(body['new_review'])
        Movie.objects.get(id=index).update(reviews=movie_reviews)
        return '', 200 
    except InvalidQueryError:
        return {'message': "Request is missing required fields"}, 400
    except DoesNotExist:
        return {'message': "Updating movie added by others is forbidden"}, 400
    except Exception as e:
        return {'message': "Something went wrong"}, 500

@app.route('/review/search/<query>', methods=['GET'])
def search_review(query):
    movies = Movie.objects()
    results = []
    for movie in movies:
        for review in movie.reviews:
            if query in review.lower():
                results.append(movie)
    return {'results': results}, 200

# score related routes

# get all scores of a movie using movie ID
@jwt_required
@app.route('/scores/<index>', methods=['GET'])
def get_scores(index):
    try:
        movie = Movie.objects.get(id=index)
        movie_scores = movie['all_scores']
        agg_score = movie['score']
        movie_scores = list(movie_scores)
        calc_agg_score = sum(movie_scores)/len(movie_scores)
        if type(agg_score) != float:
            agg_score = calc_agg_score
        return {'scores': movie_scores, 'agg_score': agg_score}, 200
    except InvalidQueryError:
        return {'message': "Request is missing required fields"}, 400
    except DoesNotExist:
        return {'message': "Updating movie added by others is forbidden"}, 400
    except Exception as e:
        return {'message': "Something went wrong"}, 500

# add new movie score
@jwt_required
@app.route('/scores/<index>', methods=['PUT'])
def update_score(index):
    try:
        body = request.get_json(force=True)
        movie_scores = Movie.objects.get(id=index)['all_scores']
        movie_scores = list(movie_scores)
        movie_scores.append(body['new_score'])
        agg_score = sum(movie_scores)/len(movie_scores)
        Movie.objects.get(id=index).update(all_scores=movie_scores, score=agg_score)
        return '', 200 
    except InvalidQueryError:
        return {'message': "Request is missing required fields"}, 400
    except DoesNotExist:
        return {'message': "Updating movie added by others is forbidden"}, 400
    except Exception as e:
        return {'message': "Something went wrong"}, 500

# return movies that have score higher than threshold
@app.route('/scores/filter/<query>', methods=['GET'])
def filter_by_score(query):
    movies = Movie.objects()
    threshold = float(query)
    results = []
    for movie in movies:
        if movie.score >= threshold:
            results.append(movie)
    return {'results': results}, 200

# return movies that have a specific score
@app.route('/scores/search/<query>', methods=['GET'])
def search_by_score(query):
    movies = Movie.objects()
    threshold = float(query)
    results = []
    for movie in movies:
        if movie.score == threshold:
            results.append(movie)
    return {'results': results}, 200

# highest scoring movie
@app.route('/scores/high/', methods=['GET'])
def best_movie():
    movie = Movie.objects().order_by("-agg_score").limit(1).first()
    return {'results': movie}, 200

# return n highest scoring movies
@app.route('/scores/high/<number>', methods=['GET'])
def best_movies(number):
    movie = Movie.objects().order_by("-agg_score").limit(int(number))
    return {'results': movie}, 200

# return n worst scoring movies
@app.route('/scores/low/<number>', methods=['GET'])
def worst_movies(number):
    movie = Movie.objects().order_by("agg_score").limit(int(number))
    return {'results': movie}, 200

# return movies that have a specific genre
@app.route('/genre/search/<query>', methods=['GET'])
def search_genre(query):
    movies = Movie.objects()
    results = []
    for movie in movies:
        if query in movie.genres:
            results.append(movie)
    return {'results': results}, 200

# return movies that have a specific cast member
@app.route('/cast/search/<query>', methods=['GET'])
def search_cast(query):
    movies = Movie.objects()
    results = []
    for movie in movies:
        if query in movie.cast:
            results.append(movie)
    return {'results': results}, 200

# box office related queries
@app.route('/money/filter/<query>', methods=['GET'])
def filter_by_box_office_collection(query):
    movies = Movie.objects()
    threshold = float(query)
    results = []
    for movie in movies:
        if movie.box_office >= threshold:
            results.append(movie)
    return {'results': results}, 200

# highest grossing movie
@app.route('/money/high', methods=['GET'])
def most_profitable_movie():
    movie = Movie.objects().order_by("-box_office").limit(1).first()
    return {'results': movie}, 200

# least grossing movie
@app.route('/money/low', methods=['GET'])
def least_profitable_movie():
    movie = Movie.objects().order_by("-box_office").limit(1).first()
    return {'results': movie}, 200

# return n highest grossing movies
@app.route('/money/highest/<number>', methods=['GET'])
def highest_grossing_movies(number):
    movie = Movie.objects().order_by("-agg_score").limit(int(number))
    return {'results': movie}, 200
