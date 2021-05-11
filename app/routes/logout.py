from flask import url_for
from werkzeug.utils import redirect

import util.logging


@util.logging.log_decorator()
def logout():
    return redirect(url_for('get_all_posts'))