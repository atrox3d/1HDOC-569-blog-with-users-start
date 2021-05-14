import flask_login
from flask import render_template, flash, url_for
from flask_login import current_user
from werkzeug.utils import redirect

from util.logutils import loghelpers
from app.forms import CommentForm
from app.models import BlogPost, Comment, db


# @flask_login.login_required
@loghelpers.log_decorator()
def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    commentform = CommentForm()
    #
    #   POST
    #
    if commentform.validate_on_submit():
        if not current_user.is_authenticated:
            flash("you need to be logged in to add a comment")
            url = url_for('login')
            return redirect(url)

        comment = Comment(
            text=commentform.comment.data,
            parent_post=requested_post,
            comment_author=current_user
        )
        db.session.add(comment)
        db.session.commit()
    #
    #
    #   GET
    #
    return render_template(
        "post.html",
        post=requested_post,
        form=commentform
        # loggedin=current_user.is_authenticated
    )
