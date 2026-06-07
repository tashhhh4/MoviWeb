from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    director = db.Column(db.String(2000))
    year = db.Column(db.String(12))
    poster_url = db.Column(db.String(300), default=None)
    
    # Each movie is "owned" by a user and each list of movies is entirely
    # maintained by the user that owns them.
    user_id = db.Column(db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="movies")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)

    movies = db.relationship("Movie", back_populates="user")

    def __str__(self):
        return self.name