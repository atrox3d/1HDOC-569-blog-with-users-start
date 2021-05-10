########################################################################################################################
# https://www.udemy.com/course/100-days-of-code/learn/lecture/22867475#questions
########################################################################################################################
#
#   Flask imports
#
########################################################################################################################
# import flask_sqlalchemy
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    # request,
)
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import (
    current_user,
    LoginManager,
    login_user
)
from werkzeug.security import (
    check_password_hash
)
########################################################################################################################
#
#   standard imports
#
########################################################################################################################
from datetime import date
import logging
########################################################################################################################
#
#   project imports
#
########################################################################################################################
from app.forms import CreatePostForm
#
# https://stackoverflow.com/questions/51756650/using-proper-file-structure-with-sqlalchemy-and-how-to-add-data-to-db
# https://github.com/slezica/bleg/blob/master/data/posts/2014-03-08-avoiding-circular-dependencies-in-flask.md
#
from app.models import (
    db,
    User,
    BlogPost
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
@app.route('/')
@util.logging.log_decorator()
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


from app.routes.register import register
register = app.route('/register', methods=['GET', 'POST'])(register)



@app.route('/login', methods=["GET", "POST"])
@util.logging.log_decorator()
def login():
    from app.forms import Loginform
    form = Loginform()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                url = url_for("get_all_posts")
                logger.info(f"redirect: {url=}")
                return redirect(url)
        else:
            url = url_for("register", loggedin=current_user.is_authenticated)
            logger.info(f"redirect: {url=}")
            return redirect(url)
    return render_template("login.html", form=form)


@app.route('/logout')
@util.logging.log_decorator()
def logout():
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>")
@util.logging.log_decorator()
def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    return render_template("post.html", post=requested_post)


@app.route("/about")
@util.logging.log_decorator()
def about():
    return render_template("about.html")


@app.route("/contact")
@util.logging.log_decorator()
def contact():
    return render_template("contact.html")


@app.route("/new-post")
@util.logging.log_decorator()
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>")
@util.logging.log_decorator()
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)


@app.route("/delete/<int:post_id>")
@util.logging.log_decorator()
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(
        # host='0.0.0.0',
        host=util.network.get_ipaddress(),
        port=5000,
        debug=True
    )
