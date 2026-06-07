from models import db, User, Movie


class DataManager():
    # Defined CRUD Operations

    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_users(self):
        users = db.session.execute(db.select(User).order_by(User.name)).scalars().all()
        return users

    def get_user(self, user_id):
        user = db.get_or_404(User, user_id)
        return user

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

    def add_movie(self, movie):
        db.session.add(movie)
        db.session.commit()
        return movie

    def get_movies(self, user_id):
        user = db.get_or_404(User, user_id)
        return user.movies

    def update_movie(self, movie_id, new_title):
        movie = db.get_or_404(Movie, movie_id)
        movie.title = new_title
        db.session.commit()
        return movie

    def delete_movie(self, movie_id):
        movie = db.get_or_404(Movie, movie_id)
        db.session.delete(movie)
        db.session.commit()
        return movie