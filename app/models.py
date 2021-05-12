from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
#
# https://stackoverflow.com/questions/51756650/using-proper-file-structure-with-sqlalchemy-and-how-to-add-data-to-db
# https://github.com/slezica/bleg/blob/master/data/posts/2014-03-08-avoiding-circular-dependencies-in-flask.md
#
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash

import util.logging
import logging
logger = logging.getLogger(__name__)

# from main import db
db = SQLAlchemy()


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    # plainpassword = db.Column(db.String(100))
    posts = relationship("BlogPost", back_populates="author")


class BlogPost(db.Model):

    __tablename__ = "blog_posts"

    id = db.Column(db.Integer, primary_key=True)
    # author = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    #
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")


@util.logging.log_decorator()
def createuser(email, password, name, id=None):
    logger.info(f"create User(")
    logger.info(f"\t{id=}, ")
    logger.info(f"\t{email=}, ")
    logger.info(f"\t{password=}, ")
    logger.info(f"\t{name=}")
    logger.info(f")")

    user = User(
        id=id,
        email=email,
        password=password,
        name=name
    )
    return user


@util.logging.log_decorator()
def adduser(user:User):
    logger.info("hash password")
    password_hash = generate_password_hash(user.password, method="pbkdf2:sha256", salt_length=8)
    user.password = password_hash
    logger.info(f"save User(")
    logger.info(f"\t{user.id=}, ")
    logger.info(f"\t{user.email=}, ")
    logger.info(f"\t{user.password=}, ")
    logger.info(f"\t{user.name=}")
    logger.info(f")")
    db.session.add(user)
    db.session.commit()