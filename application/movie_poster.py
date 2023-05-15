# import requests
# from dotenv import load_dotenv
# import os

# load_dotenv()

# base_url = "http://www.omdbapi.com/"
# api_key = os.getenv("OMDB_API_KEY")

# def get_movie_poster_url(movie_name):
#     response = requests.get(base_url, params={"apikey": api_key, "t": movie_name})
#     data = response.json()
#     print(data)
#     if(data["Response"] == "False" or "Poster" not in data or data["Poster"] == "N/A"):
#         return "https://img.kpopmap.com/2019/06/BIGGER.jpg"
#     poster_url = data["Poster"]
#     print(data["Actors"])
#     print(data["Director"])
#     return poster_url


# print(get_movie_poster_url("Toy Story"))

st = "Animation|Children's|Comedy"
print(st.split('|'))