import requests
import os

headers = {
    'x-rapidapi-host': os.environ.get('imdb_host'),
    'x-rapidapi-key': os.environ.get('imdb_key')
    }

def getMovie(id):
    url = "https://imdb-internet-movie-database-unofficial.p.rapidapi.com/film/"+id
    response = requests.request("GET", url, headers=headers)
    response.encoding='utf-8'
    data = response.json()
    return data

def Search(name):
    url = "https://imdb-internet-movie-database-unofficial.p.rapidapi.com/search/"+name
    response = requests.request("GET", url, headers=headers)
    response.encoding = 'utf-8'
    data = response.json()
    return data


