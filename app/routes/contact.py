from flask import render_template
from flask_login import current_user
from util.logutils import loghelpers


@loghelpers.log_decorator()
def contact():
    return render_template(
        "contact.html",
        # loggedin=current_user.is_authenticated
    )