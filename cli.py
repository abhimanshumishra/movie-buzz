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
\t23. See lowest grossing movies \n \
\t24. See all information about a movie\n \
\t25. Exit \n \
"

def movie_id_map():
    # {'name': 'id'}
    all_movies = cli_utils.get_movies()
    movie_to_id_map = {}
    for item in all_movies:
        movie = Movie(item)
        movie_to_id_map[movie.name] = item['_id']['$oid']
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
            break
        elif choice == 1:
            users = cli_utils.get_users()
            for user in users:
                print(user['email'])
            break
        elif choice == 2:
            query = input('Enter search query: ')
            search_results = cli_utils.search_movie_by_name(query)['results']
            if len(search_results) == 0:
                print('No matching movie found')
            for result in search_results:
                movie = Movie(result)
                movie.get_all_information()
            break
        elif choice == 3:
            query = input('Enter cast member name: ')
            search_results = cli_utils.search_by_cast(query)['results']
            if len(search_results) == 0:
                print('No matching movie found')
            for result in search_results:
                movie = Movie(result)
                movie.get_all_information()
            break
        elif choice == 4:
            query = input('Enter genre: ')
            search_results = cli_utils.search_by_genre(query)['results']
            if len(search_results) == 0:
                print('No matching movie found')
            for result in search_results:
                movie = Movie(result)
                movie.get_all_information()
            break
        elif choice == 5:
            pass
        elif choice == 6:
            pass
        elif choice == 7:
            pass
        elif choice == 8:
            pass
        elif choice == 9:
            pass
        elif choice == 10:
            pass
        elif choice == 11:
            query = input('Enter search query: ')
            search_results = cli_utils.search_movie_by_review(query)['results']
            if len(search_results) == 0:
                print('No matching movie found')
            for result in search_results:
                movie = Movie(result)
                movie.get_all_information()
            break
        elif choice == 12:
            pass
        elif choice == 13:
            pass
        elif choice == 14:
            query = input('Enter threshold: ')
            search_results = cli_utils.filter_movie_by_score(query)['results']
            if len(search_results) == 0:
                print('No matching movie found')
            for result in search_results:
                movie = Movie(result)
                movie.get_all_information()
            break
        elif choice == 15:
            query = input('Enter score: ')
            search_results = cli_utils.search_movie_by_score(query)['results']
            if len(search_results) == 0:
                print('No matching movie found')
            for result in search_results:
                movie = Movie(result)
                movie.get_all_information()
            break
        elif choice == 16:
            pass
        elif choice == 17:
            pass
        elif choice == 18:
            pass
        elif choice == 19:
            pass
        elif choice == 20:
            pass
        elif choice == 21:
            pass
        elif choice == 22:
            pass
        elif choice == 23:
            pass
        elif choice == 24:
            break
        else:
            print('Invalid input')
    print('Thank you for choosing Movie-DB!')

def main():
    menu()

if __name__ == '__main__':
    main()