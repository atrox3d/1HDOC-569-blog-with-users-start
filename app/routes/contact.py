from flask import render_template
from flask_login import current_user
import util.logging


@util.logging.log_decorator()
def contact():
    return render_template(
        "contact.html",
        # loggedin=current_user.is_authenticated
    )