from datetime import date

from flask import url_for, render_template
from flask_login import current_user
from werkzeug.utils import redirect

from util.logutils import loghelpers
from app.admin import adminonly
from app.forms import CreatePostForm
from app.models import BlogPost, db


@loghelpers.log_decorator()
@adminonly
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
    return render_template(
        "make-post.html",
        form=form,
        # loggedin=current_user.is_authenticated
    )