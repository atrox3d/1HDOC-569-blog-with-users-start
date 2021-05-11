from flask import url_for, render_template
from flask_login import current_user
from werkzeug.utils import redirect

import util.logging
from app.forms import CreatePostForm
from app.models import BlogPost, db


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
        return redirect(
            url_for(
                "show_post",
                post_id=post.id,
                # loggedin=current_user.is_authenticated
            )
        )

    return render_template(
        "make-post.html",
        form=edit_form,
        # loggedin=current_user.is_authenticated
    )
