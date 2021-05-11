from flask import render_template
from flask_login import current_user

import util.logging
import logging

logger = logging.getLogger(__name__)

@util.logging.log_decorator()
def about():
    # logger.debug(f"{current_user=}")
    # logger.debug(f"{current_user.__dict__=}")
    return render_template(
        "about.html",
        # loggedin=current_user.is_authenticated
    )