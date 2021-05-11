from flask import render_template

import util.logging


@util.logging.log_decorator()
def contact():
    return render_template("contact.html")