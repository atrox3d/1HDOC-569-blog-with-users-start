from flask import render_template

import util.logging


@util.logging.log_decorator()
def about():
    return render_template("about.html")