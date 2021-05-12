########################################################################################################################
# https://www.udemy.com/course/100-days-of-code/learn/lecture/22867475#questions
########################################################################################################################
#
#   Flask imports
#
########################################################################################################################
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import LoginManager
########################################################################################################################
#
#   standard imports
#
########################################################################################################################
import logging
########################################################################################################################
#
#   project imports
#
########################################################################################################################
#
# https://stackoverflow.com/questions/51756650/using-proper-file-structure-with-sqlalchemy-and-how-to-add-data-to-db
# https://github.com/slezica/bleg/blob/master/data/posts/2014-03-08-avoiding-circular-dependencies-in-flask.md
#
from app.admin import fix_admin
from app.models import (
    db,
    User
)
import util.network
import util.logging

########################################################################################################################
util.logging.get_root_logger()
logger = logging.getLogger(__name__)
#
#   app
#
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)
#
#   CONNECT TO DB
#
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
########################################################################################################################
#
#   resolve circular dependencies
#
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/
#
app.app_context().push()
#
# https://stackoverflow.com/questions/51756650/using-proper-file-structure-with-sqlalchemy-and-how-to-add-data-to-db
# https://github.com/slezica/bleg/blob/master/data/posts/2014-03-08-avoiding-circular-dependencies-in-flask.md
#
# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy(app)
db.init_app(app)
########################################################################################################################
# CREATE TABLE IN DB
# db.drop_all()
db.create_all()
fix_admin()
########################################################################################################################
#
#   security
#
########################################################################################################################
loginmanager = LoginManager(app)


@loginmanager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    return user


########################################################################################################################
#
#
#   routes
#
#
########################################################################################################################
from app.routes.home import get_all_posts

get_all_posts = app.route('/')(get_all_posts)

from app.routes.register import register

register = app.route('/register', methods=['GET', 'POST'])(register)

from app.routes.login import login

login = app.route('/login', methods=["GET", "POST"])(login)

from app.routes.logout import logout

logout = app.route('/logout')(logout)

from app.routes.showpost import show_post

show_post = app.route("/post/<int:post_id>")(show_post)

from app.routes.about import about

about = app.route("/about")(about)

from app.routes.contact import contact

contact = app.route("/contact")(contact)

from app.routes.addpost import add_new_post

add_new_post = app.route("/new-post")(add_new_post)

from app.routes.editpost import edit_post

edit_post = app.route("/edit-post/<int:post_id>")(edit_post)

from app.routes.deletepost import delete_post

delete_post = app.route("/delete/<int:post_id>")(delete_post)

if __name__ == "__main__":
    app.run(
        # host='0.0.0.0',
        host=util.network.get_ipaddress(),
        port=5000,
        debug=True
    )
