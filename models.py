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

    #relationships
    users = db.relationship("User",cascade="all, delete")

    def __repr__(self):
        return f'<Post: {self.title}, {self.content}, {self.created_at}>'


class Tag(db.Model):

    __tablename__= "tags"

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    name = db.Column(
        db.String(30),
        unique = True
    )
    #relationships
    assignments = db.relationship('PostTag',backref='tags')

    posts = db.relationship('Post',secondary='posts_tags',backref='tags')

class PostTag(db.Model):

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer,
        db.ForeignKey("posts.id"),
        primary_key = True,
        nullable = False
    )

    tag_id = db.Column(db.Integer,
        db.ForeignKey("tags.id"),
        primary_key = True,
        nullable = False
    )



