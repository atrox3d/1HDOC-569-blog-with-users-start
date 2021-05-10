from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
#
# https://stackoverflow.com/questions/51756650/using-proper-file-structure-with-sqlalchemy-and-how-to-add-data-to-db
# https://github.com/slezica/bleg/blob/master/data/posts/2014-03-08-avoiding-circular-dependencies-in-flask.md
#
db = SQLAlchemy()

# from main import db


##CONFIGURE TABLES
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    # plainpassword = db.Column(db.String(100))
