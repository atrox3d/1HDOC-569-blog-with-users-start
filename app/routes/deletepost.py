from flask import url_for
from werkzeug.utils import redirect

import util.logging
from app.models import BlogPost, db


@util.logging.log_decorator()
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))