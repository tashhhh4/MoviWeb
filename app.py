import os
from models import db, Movie
from flask import Flask, render_template, redirect, request, url_for, abort
from data_manager import DataManager
from movie_lookup import get_movie_details

app = Flask(__name__)


# Configure database

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'sqlite:///{os.path.join(basedir, "data/data.sqlite")}')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

dm = DataManager()


# Param helpers

class MissingParamError(Exception):
    pass


def extract_required(dict, key):
    """ Throws an error if dict[key] is empty or None. """
    value = dict.get(key, None)
    if value is None or value == '':
        raise MissingParamError()
    return value

def extract_optional(dict, key):
    """ Allows dict[key] to be None, and returns empty string as None. """
    value = dict.get(key, None)
    if value == '':
        value = None
    return value


# Routes

@app.route('/')
def home():
    return list_users()


@app.route('/users', methods=['GET'])
def list_users():
    users = dm.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def create_user():
    try:
        name = extract_required(request.form, 'name')
        dm.create_user(name)
        return redirect(url_for('home'))
    except MissingParamError:
        abort(400)


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_movies(user_id):
    user = dm.get_user(user_id)
    movies = dm.get_movies(user_id)
    return render_template('movies.html', user=user, movies=movies)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    user = dm.get_user(user_id)
    try:
        title = extract_required(request.form, 'title')
        year = extract_optional(request.form, 'year')
        director = None
        poster_url = None
        if year:
            year = int(year)
        movie_details = get_movie_details(title, year)
        if movie_details is None:
            pass  # Leave details as specified by the User.
        else:
            title, year, director, poster_url = movie_details
        new_movie = Movie(
            user=user,
            title=title,
            year=year,
            director=director,
            poster_url = poster_url,
        )
        dm.add_movie(new_movie)
        return redirect(url_for('get_movies', user_id=user_id))
    except MissingParamError:
        abort(400)
    except ValueError:
        abort(400)


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update',
           methods=['POST'])
def update_movie(user_id, movie_id):
    user = dm.get_user(user_id)
    movie = dm.get_movie(movie_id)
    try:
        title = extract_required(request.form, 'title')
        year = movie.year
        director = None
        poster_url = None
        if year:
            year = int(year)
        movie_details = get_movie_details(title, year)
        if movie_details is None:
            # Leave details as specified by the User.
            movie.title = title
            movie.director = director
            movie.poster_url = poster_url
            dm.update_movie(movie)
        else:
            title, year, director, poster_url = movie_details
            movie.title = title
            movie.year = year
            movie.director = director
            movie.poster_url = poster_url
            dm.update_movie(movie)
        return redirect(url_for('get_movies', user_id=user_id))
    except MissingParamError:
        abort(400)
    except ValueError:
        abort(400)


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete',
           methods=['POST'])
def delete_movie(user_id, movie_id):
    dm.delete_movie(movie_id)
    return redirect(url_for('get_movies', user_id=user_id))


# Custom Error Pages

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html',
        code=404,
        message="This page does not exist.",
    ), 404

@app.errorhandler(400)
def bad_request(e):
    return render_template('error.html',
        code=400,
        message=("Bad request. "
                 "This may happen if you to try to submit a form in a way "
                 "that wasn't intended by the developers.")
    ), 400

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html',
        code=500,
        message=("The application could not fulfill this request "
                 "due to a critical error."),
    ), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5002, debug=True)