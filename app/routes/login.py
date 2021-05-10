from flask import url_for, render_template
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import redirect

import logging

import util.logging
from app.models import User
# from main import app, logger

logger = logging.getLogger(__name__)

@util.logging.log_decorator()
def login():
    from app.forms import Loginform
    form = Loginform()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                url = url_for("get_all_posts")
                logger.info(f"redirect: {url=}")
                return redirect(url)
        else:
            url = url_for("register", loggedin=current_user.is_authenticated)
            logger.info(f"redirect: {url=}")
            return redirect(url)
    return render_template("login.html", form=form)