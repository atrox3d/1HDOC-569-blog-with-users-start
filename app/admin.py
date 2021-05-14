import logging

from util.logutils import loghelpers
from app.models import User, createuser, adduser, db

logger = logging.getLogger(__name__)


@loghelpers.log_decorator()
def load_admin():
    logger.info("loading admin user(id==1)")
    admin = User.query.get(1)
    return admin


@loghelpers.log_decorator()
def find_admin():
    _admin = create_default_admin()
    logger.info(f"filter_by {_admin.id=}")
    admin = db.session.query(User).filter_by(id=_admin.id).first()
    if not admin:
        logger.info(f"filter_by {_admin.mail=}")
        admin = db.session.query(User).filter_by(email=_admin.email).first()
    if not admin:
        logger.info(f"filter_by {_admin.name=}")
        admin = db.session.query(User).filter_by(name=_admin.name).first()
    return admin


@loghelpers.log_decorator()
def delete_admin():
    admin = find_admin()
    if admin:
        logger.info("admin found, deleting")
        db.session.delete(admin)
        db.session.commit()


@loghelpers.log_decorator()
def create_default_admin():
    admin = createuser(
        id=1,
        name="admin",
        email="admin@admin.com",
        password="admin"
    )
    return admin


@loghelpers.log_decorator()
def fix_admin():

    # only for testing
    # delete_admin()

    admin = load_admin()
    logger.info(f"{admin=}")
    if not admin:
        logger.info("admin not found, creating default")
        admin = create_default_admin()
        try:
            adduser(admin)
            logger.info("user default admin added")
            logger.info("user default admin check id==1")
            admin = find_admin()
            if admin.id != 1:
                logger.info("admin id != 1, fixing")
                # raise SystemExit(f"{admin.id=}")
                admin.id = 1
                db.session.commit()
                logger.info("user default admin updated")
            logger.info("user default admin check id ok")
        except Exception as e:
            logger.critical(repr(e))
            exit(1)
    else:
        logger.info("admin found")
    logger.info(f"{admin.id=}")
    logger.info(f"{admin.email=}")
    logger.info(f"{admin.password=}")
    logger.info(f"{admin.name=}")


@loghelpers.log_decorator()
def adminonly(func):
    import functools
    from flask_login import current_user
    from flask import abort

    @functools.wraps(func)
    def adminonly_decorator(*args, **kwargs):
        logger.info(f"{current_user.get_id()=}")
        userid = current_user.get_id()
        if userid and int(userid) == 1:
            result = func(*args, **kwargs)
            return result
        return abort(403)
    return adminonly_decorator
