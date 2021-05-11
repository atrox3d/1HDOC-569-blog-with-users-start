from flask import url_for
from flask_login import current_user
from werkzeug.utils import redirect

import util.logging


@util.logging.log_decorator()
def logout():
    return redirect(url_for('get_all_posts', loggedin=current_user.is_authenticated))