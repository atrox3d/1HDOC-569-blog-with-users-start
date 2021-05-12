import logging
import util.logging
from app.models import User, createuser, adduser, db

logger = logging.getLogger(__name__)


@util.logging.log_decorator()
def load_admin():
    logger.info("loading admin user(id==1)")
    admin = User.query.get(1)
    return admin


@util.logging.log_decorator()
def find_admin():
    admin = create_default_admin()
    admin = db.session.query(User).filter_by(id=admin.id).first() or \
            db.session.query(User).filter_by(name=admin.name).first() or \
            db.session.query(User).filter_by(email=admin.email).first()
    return admin


@util.logging.log_decorator()
def delete_admin():
    admin = find_admin()
    if admin:
        db.session.delete(admin)
        db.session.commit()


@util.logging.log_decorator()
def create_default_admin():
    admin = createuser(
        id=1,
        name="admin",
        email="admin@admin.com",
        password="password"
    )
    return admin


@util.logging.log_decorator()
def fix_admin():

    # delete_admin()

    admin = load_admin()
    logger.info(f"{admin=}")
    if not admin:
        logger.info("admin not found, creating default")
        admin = create_default_admin()
        try:
            adduser(admin)
            admin = find_admin()
            if admin.id != 1:
                # raise SystemExit(f"{admin.id=}")
                admin.id = 1
                db.session.commit()
        except Exception as e:
            logger.critical(repr(e))
            exit(1)
    else:
        logger.info("admin found")
    logger.info(f"{admin.id=}")
    logger.info(f"{admin.email=}")
    logger.info(f"{admin.password=}")
    logger.info(f"{admin.name=}")
