# Setup
conda create --name nep python=3.7
conda activate nep
pip install -r requirements.txt
brew tap mongodb/brew
brew install mongodb-community@4.2
# Fill in your username here - it's the folder name that shows up when you type `ls /Users` into terminal (not 'Shared')
mkdir /Users/<Username>/data
mkdir /Users/<Username>/data/db
# Run Mongo shell
# Open a terminal and type:
mongod --dbpath=/Users/<Username>/data/db
# Open a separate terminal
mongo

# Run server
# Open a terminal and type:
mongod --dbpath=/Users/<Username>/data/db
# Open a separate terminal and navigate to the correct directory
python run.py

# Run CLI
python cli.py

# Run tests
python -m unittest -b
# To run individual tests
python -m unittest -v <testname>
# There is an additional Postman test suite that can be used

# Files
app.py - Flask server routes
cli.py - Command Line Interface
cli_utils.py - Helper functions for CLI
config.py - Configurations for MongoDB and JWT
database/db.py - Initialise MongoDB database
database/models.py - Database schema and classes
run.py - Run Flask server
requirements.txt - Python package list required for project to work
tests/ - Folder with various unit tests

MongoDB is a NoSQL database so each entity can be thought of as a document or collection.
There is no relationship between two entities in such a schema.
Using database models for movies and users allows us to handle data easily and simplifies how we write out queries.
We use flask-mongoengine to connect to mongoDB using Python and Flask. 
It is built on top of PyMongo.
We wrote the queries in Mongo, and then converted them to work with flask-mongoengine.

# Database Schema
Movie(name, casts, genres, reviews, all_scores, score, box_office)
User(email, password)

# Queries

Here, we list all the queries in the raw Mongo format and converted to use with flask-mongoengine.
The queries on the left are the ones in raw Mongo format, while the ones on the right (separated by '=>') are compatible with flask-mongoengine.

## Create

#### Insert a movie
db.insert_one(Movie) => Movie.save()
#### Insert multiple movies
db.insert_many([Movie1, Movie2]) => Movie.objects.insert([Movie1, Movie2])
#### Insert a user
db.insert_one(User) => User.save()

## Read

### Select
#### Find movie by query in name
db.Movie.find({'name': {$regex: ".*"+query+".*/i"}}) => Movie.objects(name__icontains=query)
#### Find movies with particular score
db.Movie.find({'score': query}) => Movie.objects(score=query)
#### Find movies with score higher than a threshold
db.Movie.find({'score': {"$gte": query }}) => Movie.objects(score__gte=query)
#### Find movies with box office collection higher than a threshold
db.Movie.find({'box_office': {"$gte": query }}) => Movie.objects(box_office__gte=query)
#### Find movie by query in any review
db.Movie.find({'reviews': {$regex: ".*"+query+".*/i"}}) => Movie.objects(reviews=re.compile('.*'+query+'.*', re.IGNORECASE))
#### Find movie by query in any genre
db.Movie.find({'genres': {$regex: ".*"+query+".*/i"}}) => Movie.objects(genres=re.compile('.*'+query+'.*', re.IGNORECASE))
#### Find movie by query in any cast member name
db.Movie.find({'casts': {$regex: ".*"+query+".*/i"}}) => Movie.objects(casts=re.compile('.*'+query+'.*', re.IGNORECASE))

### Aggregation
#### Find any number of movies sorted in ascending order of box office collection
db.Movie.find().sort({'box_office': 1}).limit(number) => Movie.objects().order_by("box_office").limit(number)
#### Find any number of movies sorted in ascending order of rating
db.Movie.find().sort({'score': 1}).limit(number) => Movie.objects().order_by("score").limit(number)
#### Find any number of movies sorted in descending order of box office collection
db.Movie.find().sort({'box_office': -1}).limit(number) => Movie.objects().order_by("-box_office").limit(number)
#### Find any number of movies sorted in descending order of rating
db.Movie.find().sort({'score': -1}).limit(number) => Movie.objects().order_by("-score").limit(number)

## Update

#### Add new rating to movie and update overall rating using movie index
db.update_one({'id': index}, {"$set": {'all_scores': updated_scores, 'score': updated_agg_score}}) => Movie.objects.get(id=index).update(all_scores=updated_scores, score=updated_agg_score)

#### Add new review to movie using movie index
db.update_one({'id': index}, {"$set": {'reviews': updated_reviews}}) => Movie.objects.get(id=index).update(reviews=updated_reviews)

#### Update any part of movie information (overwrites previous version) using movie index
db.update_one({'id': index}, {"$set": {'name': updated_name, 'casts': updated_casts, 'genres': updated_genres, 'reviews': updated_reviews, 'all_scores': updated_all_scores, 'score': updated_score, 'box_office': updated_box_office}}) => Movie.objects.get(id=index).update(movie_data)

## Delete

#### Delete a movie using movie index
db.delete_one({'id': index}) => Movie.objects.get(id=index).delete()
#### Delete all movies
db.Movie.drop() => Movie.drop_collection()
#### Delete all users
db.User.drop() => User.drop_collection()
