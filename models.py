from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()
def connect_db(app):
    db.app = app
    db.init_app(app)


"""Models for Blogly."""
class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    first_name = db.Column(
        db.String(30),
        nullable = False,
    )

    last_name = db.Column(
        db.String(30),
        nullable = False
    )

    image_url = db.Column(
        db.Text,
        nullable = False,
        default = 'No image File Available'
    )

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        return f'<User: {self.full_name}>, {self.image_url}'


class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    title = db.Column(
        db.Text,
        nullable = False
    )

    content = db.Column(
        db.Text,
        nullable = False
    )

    created_at = db.Column(
        db.DateTime,
        default = datetime.datetime.utcnow,
    )

    user_id  = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )

    users = db.relationship("User")


