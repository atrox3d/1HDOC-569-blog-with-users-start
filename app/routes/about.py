from flask import render_template
from flask_login import current_user

from util.logutils import loghelpers
import logging

logger = logging.getLogger(__name__)

@loghelpers.log_decorator()
def about():
    # logger.debug(f"{current_user=}")
    # logger.debug(f"{current_user.__dict__=}")
    return render_template(
        "about.html",
        # loggedin=current_user.is_authenticated
    )