import os
from models import db, Movie
from flask import Flask, render_template, redirect, request
from data_manager import DataManager

app = Flask(__name__)


# Configure database

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'sqlite:///{os.path.join(basedir, "data/data.sqlite")}')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

dm = DataManager()


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
    name = request.form['name']
    dm.create_user(name)
    return redirect(url_for('home'))

@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_movies(user_id):
    user = dm.get_user(user_id)
    movies = dm.get_movies(user_id)
    return render_template('movies.html', user=user, movies=movies)

@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    # add movie by title with user as FK ("owner")
    # Try to retrieve rest of movie info from OMDB API
    return redirect(url_for('get_movies', user_id=user_id))

@app.route('/users/<int:user_id>/movies/<int:movie_id>/update',
           methods=['POST'])
def update_movie(user_id, movie_id):
    # update the movie with new title
    # Try to retrieve rest of movie info from OMDB API
    return redirect(url_for('get_movies', user_id=user_id))

@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete',
           methods=['POST'])
def delete_movie(user_id, movie_id):
    # delete the movie with the specified `movie_id`
    return redirect(url_for('get_movies', user_id=user_id))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5002, debug=True)