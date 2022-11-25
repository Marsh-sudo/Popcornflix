from urllib import response
import requests

API_KEY = "d8746dddc86e43824b569e623e4a4425"

def get_movie():
    response = requests.get(f"https://api.themoviedb.org/3/movie/550?api_key={API_KEY}")
    return response.json()

def get_popular():
    response = requests.get(f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}")
    return response.json()

def get_Upcoming():
    response = requests.get(f"https://api.themoviedb.org/3/movie/upcoming?api_key={API_KEY}")
    return response.json()

def get_Toprated():
    response = requests.get(f"https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}")
    return response.json()


def get_Nowplaying():
    response = requests.get(f"https://api.themoviedb.org/3/movie/now_playing?api_key={API_KEY}")
    return response.json()


def get_genres(list_id):
    response = requests.get(f"https://api.themoviedb.org/3/list/{list_id}?api_key={API_KEY}")
    return response.json()

def get_trending():
    response = requests.get(f"https://api.themoviedb.org/3/trending/all/day?api_key={API_KEY}")
    return response.json()

def get_video(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}")
    return response.json()