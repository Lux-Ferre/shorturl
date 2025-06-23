from flask import Blueprint, render_template, abort, redirect
from flask_security import login_required, roles_required

from sqlalchemy.exc import SQLAlchemyError

from app.models import ShortenedURL

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("main/index.html")


@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("main/dashboard.html")


@bp.route("/admin")
@roles_required("admin")
def admin():
    return render_template("main/admin.html")


@bp.route("/about")
def about():
    return render_template("main/about.html")


@bp.route("/l/<short_url>")
def redirection(short_url):
    if short_url is None:
        return abort(404)

    try:
        entry = ShortenedURL.query.filter_by(short_url=short_url).first()

        if entry is None:
            return abort(404)
    except SQLAlchemyError as e:
        print(e)
        return abort(404)

    return redirect(entry.full_url)
