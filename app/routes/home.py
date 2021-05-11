from flask import render_template

import util.logging
from app.models import BlogPost
# from main import app


@util.logging.log_decorator()
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)