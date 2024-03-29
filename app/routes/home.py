from flask import render_template
from flask_login import current_user

from util.logutils import loghelpers
from app.models import BlogPost
# from main import app


@loghelpers.log_decorator()
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template(
        "index.html",
        all_posts=posts,
        # loggedin=current_user.is_authenticated
    )