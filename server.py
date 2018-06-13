from flask import Flask, session, request, redirect, render_template, flash, url_for
from db.data_layer import get_show, create_user, login_user, get_user_by_id, create_like, get_user_likes, delete_like
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = '8118d0875ad5b6b3ad830b956b111fb0'
csrf = CSRFProtect(app)


@app.route('/')
def index():
    movies = []
    if 'user_id' in session:
        user = get_user_by_id(session['user_id'])
        movies = get_user_likes(user.id)
        return render_template('index.html', movies=movies, user_id=user.id)
    else:
        return render_template('index.html', movies=movies)


@app.route('/authenticate')
def authenticate():
    return render_template('authenticate.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['html_fullname']
    email = request.form['html_email']
    password = request.form['html_password']
    confirm = request.form['html_confirm']

    user = create_user(name, email, password, confirm)

    if user:
        session['user_id'] = user.id
        session['name'] = user.name
        return redirect(url_for('index'))
    else:
        for messages in user:
            flash(messages)
        return redirect(url_for('authenticate'))


@app.route('/login', methods=['POST'])
def login():
    email = request.form['html_email']
    password = request.form['html_password']
    
    user = login_user(email, password)
    
    if user:
        session['user_id'] = user.id
        session['name'] = user.name
        return redirect(url_for('index'))
    else:
        for messages in user:
            flash(messages)
        return redirect(url_for('authenticate'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search_query():
    query = request.form['query']
    return redirect(url_for('search', query=query))

@app.route('/search/<query>')
def search(query):
    movies = get_show(query)
    if 'user_id' in session:
        likes = get_user_likes(session['user_id'])
        liked = {}
        
        for like in likes:
            liked[like.movie.api_id] = True
    else:
        liked = {}

    return render_template('search.html', movies=movies, liked=liked)

@app.route('/like/<movie_id>')
def create_user_like(movie_id):
    user = get_user_by_id(session['user_id'])
    create_like(user.id, movie_id)
    url = request.headers['Referer']
    return redirect(url)

@app.route('/unlike/<movie_id>')
def delete_user_like(movie_id):
    user = get_user_by_id(session['user_id'])
    delete_like(movie_id)
    url = request.headers['Referer']
    return redirect(url)

@app.route('/user/<user_id>')
def get_like(user_id):
    movies = get_user_likes(user_id)
    return render_template('like.html', movies=movies)

app.jinja_env.auto_reload = True
app.config['TEMPLATE_AUTO_RELOAD'] = True

app.run(debug=True, use_reloader=True)
