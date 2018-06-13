import re, bcrypt, json, requests
from sqlalchemy import desc

from flask_wtf.csrf import CSRFProtect

from db.base import DbManager
from db.models import User, Movie, Like

db = DbManager()
EMAIL_REGEX = re.compile(r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$')

API_URL = 'http://api.tvmaze.com/search/shows?q={}'

def get_request(url):
    response = requests.get(url)
    return json.loads(response.text)

def is_blank(name, field, messages):
    if len(field) == 0:
        messages.append('Len {} to short'.format(name))
        return True
    else:
        return False

def get_user_by_email(email):
    db = DbManager()
    return db.open().query(User).filter(User.email == email).one()

def get_user_by_id(user_id):
    db = DbManager()
    return db.open().query(User).filter(User.id == user_id).one()

def get_movie_api_id(api_id):
    db = DbManager()
    return db.open().query(Movie).filter(Movie.api_id == api_id).one()

def get_show(query):
    db = DbManager()
    url = API_URL.format(query)
    data = get_request(url)
    movies = []

    for obj in data:
        movie = Movie()
        movie.parse_json(obj)
        
        try:
            db.open().query(Movie).filter(Movie.url == movie.url).one()
        except:
            db.save(movie)
        
        movies.append(movie)
        
    return movies

def create_user(name, email, password, confirm):

    messages = []

    is_valid = True

    is_valid = not is_blank('name', name, messages)
    is_valid = not is_blank('email', email, messages)
    is_valid = not is_blank('password', password, messages)
    is_valid = not is_blank('confirm', confirm, messages)

    if password != confirm:
        is_valid = False
        messages.append('Password doesn\'t match')
    if len(password) < 6:
        is_valid = False
        messages.append('Password too short')
    if not EMAIL_REGEX.match(email):
        is_valid = False
        messages.append('Email formated error')

    if is_valid:
        try:
            encoded = password.encode('UTF-8')
            encrypted = bcrypt.hashpw(encoded, bcrypt.gensalt())

            user = User()
            user.name = name
            user.email = email
            user.password = encrypted
            db.save(user)

            messages.append('User {} was created successfully'.format(user.name))
            
            return user
        except:
            messages.append('User already exist')

    return messages

def login_user(email, password):

    messages = []

    is_valid = True

    is_valid = not is_blank('email', email, messages)
    is_valid = not is_blank('password', password, messages)

    if len(password) < 6:
        is_valid = False
        messages.append('Password too short')
    if not EMAIL_REGEX.match(email):
        is_valid = False
        messages.append('Email formated error')

    if is_valid:
        try:
            user = get_user_by_email(email)
            encoded = password.encode('UTF-8')
            if bcrypt.checkpw(encoded, user.password):
                messages.append('Login successfully')
                return user
        except:
            messages.append('Login error')

    return messages

def create_like(user_id, movie_id):

    messages = []

    try:
        db.open().query(Like).filter(Like.user_id == user_id).filter(Like.movie_id == movie_id).one()
        messages.append('Movie ID {} already liked'.format(movie_id))
    except:
        movie = get_movie_api_id(movie_id)
        like = Like()
        like.user_id = user_id
        like.movie_id = movie.id
        db.save(like)
        return like

    return messages

def get_user_likes(user_id):

    messages = []
    movies = []

    try:
        likes = db.open().query(Like).filter(Like.user_id == user_id).order_by(desc(Like.created_at)).all()
        return likes
    except:
        messages.append('User ID {} has no movies liked'.format(user_id))

    return messages

def delete_like(like_id):

    messages = []

    try:
        movie = db.open().query(Movie).filter(Movie.api_id == like_id).one()
        like = db.open().query(Like).filter(Like.movie_id == movie.id).one()
        db.delete(like)
        messages.append('Movie ID {} deleted successfully'.format(movie.id))
    except:
        messages.append('Unlike Movie ID {} error'.format(movie.id))

    return messages

# add your data functions here


