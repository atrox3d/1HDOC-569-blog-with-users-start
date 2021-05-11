from flask import render_template

import util.logging
from app.models import BlogPost


@util.logging.log_decorator()
def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    return render_template("post.html", post=requested_post)