import json, requests
from db.base import DbManager
from db.models import User, Movie, Like

API_URL         = 'http://api.tvmaze.com/search/shows?q={}'
API_SHOW_URL    = 'http://api.tvmaze.com/shows/{}'

def get_request(url):
    response = requests.get(url)
    return json.loads(response.text)

def get_movie_all(url):
    data = get_request(url)
    movies = []
    for result in data:
        movies.append(result)
        print(result)
        print('++++++')
    return result

def create_like(user_id, movie_id):
    url = API_SHOW_URL.format(movie_id)
    data = get_request(url)

    print(data)

    movie = Movie()
    movie.parse_json2(data)

    like = Like()
    like.user_id = user_id
    like.show_id = data.id

    return

def get_movie(show_id):
    url = API_SHOW_URL.format(show_id)
    movie = get_request(url)
    return movie

def search_movie(query):
    url = API_URL.format(query)
    results = get_movie_all(url)
    return results

def search_movie_by_url(url):
    try:
        db = DbManager()
        movie = db.open().query(Movie).filter(Movie.url == url).one()
        return movie
    except:
        pass

print(search_movie_by_url('http://www.tvmaze.com/shows/139/girls'))