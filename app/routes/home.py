from flask import render_template
from flask_login import current_user

import util.logutils
from app.models import BlogPost
# from main import app


@util.logutils.log_decorator()
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template(
        "index.html",
        all_posts=posts,
        # loggedin=current_user.is_authenticated
    )