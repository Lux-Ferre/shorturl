from datetime import datetime, timezone

from flask import current_app
from app.extensions import db
from flask_security import SQLAlchemyUserDatastore
from flask_security.utils import hash_password
from app.models import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)


def bootstrap_admin():
    email = current_app.config.get("DEFAULT_ADMIN_EMAIL")
    password = current_app.config.get("DEFAULT_ADMIN_PASSWORD")
    if not User.query.filter_by(email=email).first():
        admin_role = Role.query.filter_by(name="admin").first()
        if not admin_role:
            admin_role = Role(name="admin")
            db.session.add(admin_role)

        user = user_datastore.create_user(email=email, password=hash_password(password))
        user.confirmed_at = datetime.now(tz=timezone.utc)
        user.active = True
        user_datastore.add_role_to_user(user, admin_role)
        db.session.commit()
