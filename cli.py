import os
import sys

import cli_utils

class Movie():
    def __init__(self, movie):
        self.name = movie['name']
        self.casts = movie['casts']
        self.genres = movie['genres']
        self.reviews = movie['reviews']
        self.all_scores = movie['all_scores']
        self.score = movie['score']
        self.box_office = movie['box_office']
        self.movie_id = movie['_id']['$oid']

    def get_name(self):
        print(f'Movie name: {self.name}')

    def get_score(self):
        print(f'Movie rating: {self.score}')

    def get_all_scores(self):
        scores_str = ' '.join([str(s) for s in self.all_scores])
        print(f'Movie ratings: {scores_str}')

    def get_box_office(self):
        print(f'Box office collection of {self.name} is ${self.box_office}')

    def get_reviews(self):
        for review in self.reviews:
            print(review)

    def get_all_information(self):
        scores_str = ', '.join([str(s) for s in self.all_scores])
        cast_str = ', '.join([c for c in self.casts])
        genre_str = ', '.join([g for g in self.genres])
        print(f'Movie name: {self.name}; Cast: {cast_str}; Genres: {genre_str}; All ratings: {scores_str}; Overall rating: {self.score}; Box office draw: ${self.box_office}')

welcome_str = "Welcome to Movie-DB, the database course project by Abhimanshu Mishra and Ramandeep Kaur\n"

main_menu_str = "\
\tPlease select one of the options:\n \
\t1. See all movies in database\n \
\t2. See all users in database\n \
\t3. Search for a movie by its name\n \
\t4. Search for movies by a cast member\n \
\t5. Search for movies by genre\n \
\t6. Add a new user\n \
\t7. Add a new movie\n \
\t8. Update movie information \n \
\t9. Delete a movie in database \n \
\t10. See all reviews of a movie \n \
\t11. Add a review for a movie \n \
\t12. Search reviews \n \
\t13. See all ratings for a movie \n \
\t14. Add a rating for a movie \n \
\t15. See all movie that have a rating higher than a threshold \n \
\t16. Search for movies with a specific score \n \
\t17. See highest scoring movie \n \
\t18. See top scoring movies \n \
\t19. See lowest scoring movies \n \
\t20. See movies with a box office collection higher than a threshold \n \
\t21. See highest grossing movie \n \
\t22. See top grossing movies \n \
\t23. See lowest grossing movie \n \
\t24. See all information about a movie\n \
\t25. Delete all movies in database\n \
\t26. Delete all users in database\n \
\t27. Add multiple movies into database\n \
\t28. Exit \n \
"

def movie_id_map():
    all_movies = cli_utils.get_movies()
    movie_to_id_map = {}
    for item in all_movies:
        movie = Movie(item)
        movie_to_id_map[movie.name.lower()] = item['_id']['$oid']
    return movie_to_id_map

def menu():
    print(welcome_str)
    while True:
        print(main_menu_str)
        choice = int(input('Enter your choice: '))
        choice -= 1
        if choice == 0:
            movies = cli_utils.get_movies()
            for item in movies:
                movie = Movie(item)
                movie.get_all_information()
        elif choice == 1:
            users = cli_utils.get_users()
            for user in users:
                print(user['email'])
        elif choice == 2:
            query = input('Enter search query: ')
            search_results = cli_utils.search_movie_by_name(query)['results']
            if len(search_results) == 0:
                print('No matching movie found')
            for result in search_results:
                movie = Movie(result)
                movie.get_all_information()
        elif choice == 3:
            query = input('Enter cast member name: ')
            search_results = cli_utils.search_by_cast(query)['results']
            if len(search_results) == 0:
                print('No matching movie found')
            for result in search_results:
                movie = Movie(result)
                movie.get_all_information()
        elif choice == 4:
            query = input('Enter genre: ')
            search_results = cli_utils.search_by_genre(query.lower())['results']
            if len(search_results) == 0:
                print('No matching movie found')
            for result in search_results:
                movie = Movie(result)
                movie.get_all_information()
        elif choice == 5:
            email = input('Enter email: ')
            password = input('Enter password (minimum 6 characters): ')
            response = cli_utils.signup(email, password)
            if 'user_id' in response:
                print('New user created successfully')
            else:
                print(response['message'])
        elif choice == 6:
            name = input('Enter movie name: ')
            review = input('Enter review: ')
            score = float(input('Enter rating: '))
            box_office = float(input('Enter box office collection: '))
            genres, cast = [], []
            while True:
                genre = input('Add genre (N to skip): ')
                if genre.lower() == 'n' and len(genres) == 0:
                    print('You have to add atleast one genre')
                    continue
                elif genre.lower() == 'n':
                    break
                genres.append(genre)
            while True:
                member = input('Add cast member (N to skip): ')
                if member.lower() == 'n' and len(cast) == 0:
                    print('You have to add atleast one cast member')
                    continue
                elif member.lower() == 'n':
                    break
                cast.append(member)
            response = cli_utils.add_movie(name, cast, genres, [review], [score], score, box_office)
            if 'id' in response:
                print('Movie added successfully')
            else:
                print(response['message'])
        elif choice == 7:
            movie_to_idx_mapper = movie_id_map()
            name = input('Enter exact name of movie you want to update: ')
            movie_id = movie_to_idx_mapper[name.lower()]
            try:
                old_movie_information = Movie(cli_utils.get_specific_movie(movie_id))
                new_name = input('Enter new name (N to skip): ')
                new_review = input('Enter new review to overwrite all old reviews (N to skip): ')
                new_score = float(input('Enter new score (-1 to skip): '))
                new_box_office = float(input('Enter new box office collection (-1 to skip): '))
                new_genres, new_cast = [], []
                while True:
                    new_genre = input('Enter new genre (N to skip): ')
                    if new_genre.lower() == 'n':
                        break
                    new_genres.append(new_genre)
                while True:
                    new_cast_member = input('Enter new cast member (N to skip): ')
                    if new_cast_member.lower() == 'n':
                        break
                    new_cast.append(new_cast_member)
                if new_name.lower() == 'n':
                    update_name = old_movie_information.name
                else:
                    update_name = new_name
                if new_review.lower() == 'n':
                    update_review = old_movie_information.reviews
                else:
                    update_review = [new_review]
                if len(new_cast) == 0:
                    update_cast = old_movie_information.cast
                else:
                    update_cast = new_cast
                if len(new_genres) == 0:
                    update_genres = old_movie_information.genres
                else:
                    update_genres = new_genres
                if new_score == -1:
                    update_score = old_movie_information.score
                    update_all_scores = old_movie_information.all_scores
                else:
                    update_score = new_score
                    update_all_scores = [new_score]
                if new_box_office == -1:
                    update_box_office = old_movie_information.box_office
                else:
                    update_box_office = new_box_office
                cli_utils.update_movie(movie_id, update_name, update_cast, update_genres, update_review, update_all_scores, update_score, update_box_office)
            except:
                print('The movie you\'re trying to modify does not exist')
        elif choice == 8:
            movie_to_idx_mapper = movie_id_map()
            name = input('Enter exact name of movie you want to delete: ')
            movie_id = movie_to_idx_mapper[name.lower()]
            response = cli_utils.delete_movie(movie_id)
            if response == 200:
                print('successfully deleted')
            else:
                print('Something went wrong')
        elif choice == 9:
            movie_to_idx_mapper = movie_id_map()
            name = input('Enter exact name of movie you want to see reviews for: ')
            movie_id = movie_to_idx_mapper[name.lower()]
            response = cli_utils.find_review_by_movie_id(movie_id)
            reviews = response['reviews']
            for review in reviews:
                print(review)
        elif choice == 10:
            movie_name = input('Enter exact name of movie you want to add a review for: ')
            movie_id = movie_to_idx_mapper[movie_name.lower()]
            new_review = input('Enter new review: ')
            response = cli_utils.add_review(movie_id, new_review)
            if response == 200:
                print('Review added successfully')
            else:
                print('Something went wrong')
        elif choice == 11:
            query = input('Enter search query: ')
            search_results = cli_utils.search_movie_by_review(query)['results']
            if len(search_results) == 0:
                print('No matching movie found')
            for result in search_results:
                movie = Movie(result)
                movie.get_all_information()
        elif choice == 12:
            movie_to_idx_mapper = movie_id_map()
            name = input('Enter exact name of movie you want to see ratings for: ')
            movie_id = movie_to_idx_mapper[name.lower()]
            response = cli_utils.find_score_by_movie_id(movie_id)
            scores = response['all_scores']
            scores_str = ', '.join([str(s) for s in scores])
            print(scores_str)
        elif choice == 13:
            movie_to_idx_mapper = movie_id_map()
            movie_name = input('Enter exact name of movie you want to add a score for: ')
            movie_id = movie_to_idx_mapper[movie_name.lower()]
            new_score = input('Enter new score: ')
            response = cli_utils.add_new_rating(movie_id, new_score)
            if response == 200:
                print('Score added successfully')
            else:
                print('Something went wrong')
        elif choice == 14:
            query = input('Enter threshold: ')
            search_results = cli_utils.filter_movie_by_score(query)['results']
            if len(search_results) == 0:
                print('No matching movie found')
            for result in search_results:
                movie = Movie(result)
                movie.get_all_information()
        elif choice == 15:
            query = input('Enter score: ')
            search_results = cli_utils.search_movie_by_score(query)['results']
            if len(search_results) == 0:
                print('No matching movie found')
            for result in search_results:
                movie = Movie(result)
                movie.get_all_information()
        elif choice == 16:
            movie = Movie(cli_utils.highest_scoring_movie()['results'])
            movie.get_all_information()
        elif choice == 17:
            query = input('Enter number of highest scoring movies you want to see: ')
            movies = cli_utils.highest_scoring_movies(query)['results']
            for item in movies:
                movie = Movie(item)
                movie.get_all_information()
        elif choice == 18:
            query = input('Enter number of lowest scoring movies you want to see: ')
            movies = cli_utils.lowest_scoring_movies(query)['results']
            for item in movies:
                movie = Movie(item)
                movie.get_all_information()
        elif choice == 19:
            query = input('Enter box office threshold: ')
            movies = cli_utils.filter_by_box_office_collection(query)
            for item in movies:
                movie = Movie(item)
                movie.get_all_information()
        elif choice == 20:
            movie = Movie(cli_utils.highest_grossing_movie()['results'])
            movie.get_all_information()
        elif choice == 21:
            query = input('Enter number of highest grossing movies you want to see: ')
            movies = cli_utils.highest_grossing_movies(query)['results']
            for item in movies:
                movie = Movie(item)
                movie.get_all_information()
        elif choice == 22:
            movie = Movie(cli_utils.lowest_grossing_movie()['results'])
            movie.get_all_information()
        elif choice == 23:
            movie_to_idx_mapper = movie_id_map()
            name = input('Enter exact name of movie you want to see information for: ')
            movie_id = movie_to_idx_mapper[name.lower()]
            try:
                movie = Movie(cli_utils.get_specific_movie(movie_id))
                movie.get_all_information()
            except:
                print('Something went wrong')
        elif choice == 24:
            success = cli_utils.delete_all_movies()
            if success:
                print('Successfully deleted all movies')
            else:
                print('Something went wrong')
        elif choice == 25:
            success = cli_utils.delete_all_users()
            if success:
                print('Successfully deleted all users')
            else:
                print('Something went wrong')
        elif choice == 26:
            num = int(input('How many movies do you want to add? '))
            names, casts, genre_list, reviews_list, all_scores_list, score_list, box_offices = [], [], [], [], [], [], []
            for i in range(num):
                name = input('Enter movie name: ')
                review = input('Enter review: ')
                score = float(input('Enter rating: '))
                box_office = float(input('Enter box office collection: '))
                genres, cast = [], []
                while True:
                    genre = input('Add genre (N to skip): ')
                    if genre.lower() == 'n' and len(genres) == 0:
                        print('You have to add atleast one genre')
                        continue
                    elif genre.lower() == 'n':
                        break
                    genres.append(genre)
                while True:
                    member = input('Add cast member (N to skip): ')
                    if member.lower() == 'n' and len(cast) == 0:
                        print('You have to add atleast one cast member')
                        continue
                    elif member.lower() == 'n':
                        break
                    cast.append(member)
                names.append(name)
                casts.append(cast)
                genre_list.append(genres)
                reviews_list.append([review])
                all_scores_list.append([score])
                score_list.append(score)
                box_offices.append(box_office)
                response = cli_utils.add_multiple_movies(names, casts, genre_list, reviews_list, all_scores_list, score_list, box_offices)
            if response == 200:
                print('All movies added successfully')
            else:
                print('Something went wrong')
        elif choice == 27:
            break
        else:
            print('Invalid input')
    print('Thank you for choosing Movie-DB!')

def main():
    menu()

if __name__ == '__main__':
    main()