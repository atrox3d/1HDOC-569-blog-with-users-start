from flask import url_for, render_template, flash
from werkzeug.utils import redirect

import logging

import app.forms
import util.logging
from app.models import createuser, adduser

logger = logging.getLogger(__name__)

# from main import app, logger
@util.logging.log_decorator()
def processform(form: app.forms.RegisterForm):
    email = form.email.data
    password = form.password.data
    name = form.name.data
    logger.info(f"{email=}")
    logger.info(f"{password=}")
    logger.info(f"{name=}")
    return email, password, name


@util.logging.log_decorator()
def register():
    from app.forms import RegisterForm
    form = RegisterForm()
    if form.validate_on_submit():
        logger.info("POST")
        email, password, name = processform(form)
        user = createuser(email, password, name)
        try:
            adduser(user)
            url = url_for("get_all_posts")
            logger.info(f"redirect: {url=}")
            return redirect(url)
        except Exception as e:
            logger.error(repr(e))
            flash("email already in use, login instead")
            url = url_for("login")
            logger.info(f"redirect: {url=}")
            return redirect(url)
    logger.info("GET")
    return render_template(
        "register.html",
        form=form,
        # loggedin=current_user.is_authenticated
    )
