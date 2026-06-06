import os
from models import db
from flask import Flask
import models
from data_manager import DataManager

app = Flask(__name__)


# Configure database

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "data/data.sqlite")}'

db.init_app(app)

dm = DataManager()


# Routes

@app.route('/')
def index():
    return "Hello"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)

    # DB Migration
    with app.app_context():
        db.create_all()