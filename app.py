from flask import Flask, request, Response, jsonify, render_template
from database.models import Movie, User
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from database.db import initialize_db
from flask_bcrypt import Bcrypt
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError

import config
import os
import datetime
import re

app = Flask(__name__)
app.config.from_pyfile('config.py')
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

db = initialize_db(app)

def format(message, status):
    return jsonify({"message": message, "status": status})

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

@app.route('/users/all', methods=['DELETE'])
def delete_all_users():
    User.drop_collection()
    return {'results': (User.objects.first() == None)}, 200

# movie related routes

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.objects().to_json()
    return Response(movies, mimetype="application/json", status=200)

@app.route('/movies/all', methods=['DELETE'])
def delete_all_movies():
    Movie.drop_collection()
    return {'results': (Movie.objects.first() == None)}, 200

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

# add multiple new movies
@jwt_required
@app.route('/movies/many', methods=['POST'])
def add_many_movies():
    try:
        body = request.get_json(force=True)
        movies = []
        for item in body:
            movies.append(Movie(**item))
        Movie.objects.insert(movies)
        return '', 200
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
    res = Movie.objects(name__icontains=query)
    return {'results': res}, 200

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
    results = Movie.objects(reviews=re.compile('.*'+query+'.*', re.IGNORECASE))
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
        return {'all_scores': movie_scores, 'score': agg_score}, 200
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
        movie_scores.append(float(body['new_score']))
        agg_score = sum(movie_scores)/len(movie_scores)
        Movie.objects.get(id=index).update(all_scores=movie_scores, score=agg_score)
        return '', 200 
    except InvalidQueryError:
        return {'message': "Request is missing required fields"}, 400
    except DoesNotExist:
        return {'message': "Updating movie added by others is forbidden"}, 400
    except Exception as e:
        return {'message': "Something went wrong"}, 500

@app.route('/scores/filter/<query>', methods=['GET'])
def filter_by_score(query):
    results = Movie.objects(score__gte=query)
    return {'results': results}, 200

@app.route('/scores/search/<query>', methods=['GET'])
def search_by_score(query):
    results = Movie.objects(score=query)
    return {'results': results}, 200

# highest scoring movie
@app.route('/scores/high/', methods=['GET'])
def best_movie():
    movie = Movie.objects().order_by("-score").limit(1).first()
    return {'results': movie}, 200

# return n highest scoring movies
@app.route('/scores/high/<number>', methods=['GET'])
def best_movies(number):
    movie = Movie.objects().order_by("-score").limit(int(number))
    return {'results': movie}, 200

# return n worst scoring movies
@app.route('/scores/low/<number>', methods=['GET'])
def worst_movies(number):
    movie = Movie.objects().order_by("score").limit(int(number))
    return {'results': movie}, 200

@app.route('/genre/search/<query>', methods=['GET'])
def search_genre(query):
    results = Movie.objects(genres=re.compile(query, re.IGNORECASE))
    return {'results': results}, 200

@app.route('/cast/search/<query>', methods=['GET'])
def search_cast(query):
    results = Movie.objects(casts=re.compile(query, re.IGNORECASE))
    return {'results': results}, 200

@app.route('/money/filter/<query>', methods=['GET'])
def filter_by_box_office_collection(query):
    results = Movie.objects(box_office__gte=query)
    return {'results': results}, 200

# highest grossing movie
@app.route('/money/high', methods=['GET'])
def most_profitable_movie():
    movie = Movie.objects().order_by("-box_office").limit(1).first()
    return {'results': movie}, 200

# least grossing movie
@app.route('/money/low', methods=['GET'])
def least_profitable_movie():
    movie = Movie.objects().order_by("box_office").limit(1).first()
    return {'results': movie}, 200

# return n highest grossing movies
@app.route('/money/highest/<number>', methods=['GET'])
def highest_grossing_movies(number):
    movie = Movie.objects().order_by("-box_office").limit(int(number))
    return {'results': movie}, 200
