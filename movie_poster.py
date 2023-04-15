import requests

base_url = "http://www.omdbapi.com/"
api_key = "374c6e5b"

def get_movie_poster_url(movie_name):
    response = requests.get(base_url, params={"apikey": api_key, "t": movie_name})
    data = response.json()
    poster_url = data["Poster"]
    return poster_url
