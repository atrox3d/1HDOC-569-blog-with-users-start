from flask import render_template
from flask_login import current_user

import util.logging


@util.logging.log_decorator()
def about():
    return render_template("about.html", loggedin=current_user.is_authenticated)