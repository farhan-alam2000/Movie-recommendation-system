import json

with open('popularMovies2.json') as file:
    data = json.load(file)

# Get the array of movies
movies = data['popular_movies']
# Print the movies
for movie in movies:
    print(movie)