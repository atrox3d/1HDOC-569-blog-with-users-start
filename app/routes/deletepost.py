from flask import url_for
from flask_login import current_user
from werkzeug.utils import redirect

from util.logutils import loghelpers
from app.admin import adminonly
from app.models import BlogPost, db


@loghelpers.log_decorator()
@adminonly
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(
        url_for(
            'get_all_posts',
            # loggedin=current_user.is_authenticated
        )
    )