import os
from models import db, Movie
from flask import Flask, render_template
from data_manager import DataManager

app = Flask(__name__)


# Configure database

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "data/data.sqlite")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

dm = DataManager()


# Routes

@app.route('/')
def home():
    users = dm.get_users()
    return render_template('index.html', users=users)

@app.route('/users')
def list_users():
    users = dm.get_users()
    output = ''
    for user in users:
        output += str(user) + ', '
    output = output[:-2]
    return output

@app.route('/users/<int:user_id>/movies')
def get_movies(user_id):
    movies = dm.get_movies(user_id)
    return f"List of {len(movies)} Movies for User #{user_id}"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5002, debug=True)