from flask import Flask
from app.config import Config
from app.extensions import db, security
from app.models import User, Role, ShortenedURL
from app.routes.main import bp as main_bp
from app.routes.api import bp as api_bp
from app.routes.errors import bp as errors_bp
from app.routes.utils import register_hooks
from app.services.bootstrap import bootstrap_admin
from flask_security import SQLAlchemyUserDatastore


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore)

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(errors_bp)

    register_hooks(app)

    with app.app_context():
        db.create_all()
        bootstrap_admin()

    return app
