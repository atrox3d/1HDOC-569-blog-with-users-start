from flask import url_for, render_template, flash
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import redirect

import logging

import app.forms
import util.logutils
from app.models import User

# from main import app, logger

logger = logging.getLogger(__name__)


@util.logutils.log_decorator()
def processform(form: app.forms.Loginform):
    email = form.email.data
    password = form.password.data
    logger.info(f"{email=}")
    logger.info(f"{password=}")
    return email, password


@util.logutils.log_decorator()
def login():
    from app.forms import Loginform
    form = Loginform()
    if form.validate_on_submit():
        logger.info("POST")
        email,  password = processform(form)
        logger.info(f"query user {email=}")
        user = User.query.filter_by(email=email).first()
        if user:
            logger.info("found user, check password")
            if check_password_hash(user.password, password):
                logger.info("password ok, login user")
                login_user(user)
                url = url_for("get_all_posts")
                logger.info(f"redirect: {url=}")
                return redirect(url)
            else:
                logger.error("wrong password")
                flash("wrong password, try again")
        else:
            logger.error("user not found")
            flash("email not found, please register")
            url = url_for("register")
            logger.info(f"redirect: {url=}")
            return redirect(url)
    return render_template(
        "login.html",
        form=form,
        # loggedin=current_user.is_authenticated
    )
