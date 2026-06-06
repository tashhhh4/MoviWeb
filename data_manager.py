from models import db, User, Movie


class DataManager():
    # Defined CRUD Operations

    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_users(self):
        users = db.session.execute(db.select(User).order_by(User.name)).scalars()
        return users

    def update_user(self, user_id, name):
        user = db.get_or_404(User, user_id)
        user.name = name
        db.session.commit()
        return user

    def delete_user(self, user_id):
        user = db.get_or_404(User, user_id)
        db.session.delete(user)
        db.session.commit()
        return user

    def add_movie(self, user_id, title, director=None, year=None, poster_url=None):
        user = db.get_or_404(User, user_id)
        new_movie = Movie(
            title=title,
            director=director,
            year=year,
            poster_url=poster_url,
            user=user
        )
        db.session.add(new_movie)
        db.session.commit()
        return new_movie

    def get_movies(self, user_id):
        user = db.get_or_404(User, user_id)
        return user.movies

    def update_movie(self, movie_id, title=None, director=None, year=None, poster_url=None):
        movie = db.get_or_404(Movie, movie_id)
        if title:
            movie.title = title
        if director:
            movie.director = director
        if year:
            movie.year = year
        if poster_url:
            movie.poster_url = poster_url
        db.session.commit()
        return movie

    def delete_movie(self, movie_id):
        movie = db.get_or_404(Movie, movie_id)
        db.session.delete(movie)
        db.session.commit()
        return movie