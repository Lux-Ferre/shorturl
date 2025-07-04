import shortuuid

from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError

from flask import Blueprint, jsonify, request
from flask_security import roles_required, auth_required, current_user

from app.models import ShortenedURL, User
from app.extensions import db

bp = Blueprint("api", __name__)


@bp.route("/api/get_links")
@auth_required()
def get_links():
    user_id = current_user.id
    try:
        urls = dict(ShortenedURL.query.with_entities(
            ShortenedURL.short_url,
            ShortenedURL.full_url
        ).filter_by(user_id=user_id).all())
        return jsonify({"links": urls}), 200
    except SQLAlchemyError as e:
        print(e)
        return jsonify({"error_code": "GL-D-001", "error_message": "Unexpected error. Please try again."}), 400


@bp.route("/api/add_link", methods=["POST"])
@auth_required()
def add_link():
    if not request.is_json:
        return jsonify({"error_code": "AL-R-001", "error_message": "Malformed request: Invalid JSON."}), 400

    request_data = request.get_json()
    full_url = request_data.get("full_url", None)
    short_url = request_data.get("short_url", None)
    user_id = current_user.id

    if full_url is None:
        return jsonify({"error_code": "AL-F-001", "error_message": "Full URL is required."}), 400

    if not (full_url.startswith("http://") or full_url.startswith("https://")):
        full_url = "https://" + full_url

    if short_url is not None and short_url != "":
        if len(short_url) < 1 or len(short_url) > 50:
            return jsonify({"error_code": "AL-S-001", "error_message": "Short URL invalid: Must be between 1 and 50 characters."}), 400
        try:
            if ShortenedURL.query.filter_by(short_url=short_url).first() is not None:
                return jsonify({"error_code": "AL-S-002", "error_message": "Short URL invalid: Already exists."}), 400
        except SQLAlchemyError as e:
            print(e)
            return jsonify({"error_code": "AL-D-001", "error_message": "Unexpected error. Please try again."}), 400
    else:
        for i in range(3):
            short_url = shortuuid.random(length=12)
            try:
                shortuuid_exists = ShortenedURL.query.filter_by(short_url=short_url).first()
                if not shortuuid_exists:
                    break
            except SQLAlchemyError as e:
                print(e)
                return jsonify({"error_code": "AL-D-002", "error_message": "Unexpected error. Please try again."}), 400
        else:
            return jsonify({"error_code": "AL-S-003", "error_message": "Unable to generate random URL. Try creating your own."}), 400

    try:
        new_entry = ShortenedURL(
            user_id=user_id,
            short_url=short_url,
            full_url=full_url
        )

        db.session.add(new_entry)
        db.session.commit()

        return jsonify({"short_url": short_url, "full_url": full_url}), 200
    except SQLAlchemyError as e:
        print(e)
        return jsonify({"error_code": "AL-D-003", "error_message": "Unexpected error. Please try again."}), 400


@bp.route("/api/get_pending")
@roles_required("admin")
def get_pending():
    try:
        unconfirmed_users = dict(db.session.query(User.id, User.email).filter(User.confirmed_at.is_(None)).all())
        return jsonify({"unconfirmed_users": unconfirmed_users}), 200
    except SQLAlchemyError as e:
        print(e)
        return jsonify({"error_code": "GP-D-001", "error_message": "Unexpected error. Please try again."}), 400


@bp.route("/api/approve_user", methods=["POST"])
@roles_required("admin")
def approve_user():
    if not request.is_json:
        return jsonify({"error_code": "AU-R-001", "error_message": "Malformed request: Invalid JSON."}), 400

    request_data = request.get_json()
    user_id = request_data.get("user_id", None)

    if user_id is None:
        return jsonify({"error_code": "AU-U-001", "error_message": "Malformed request: User ID required."}), 400

    try:
        user = User.query.get(user_id)
        if user:
            user.confirmed_at = datetime.now(tz=timezone.utc)
            db.session.commit()
            return jsonify({"confirmed_user": user_id}), 200
        return jsonify({"error_code": "AU-U-002", "error_message": f"User {user_id} not found."}), 400
    except SQLAlchemyError as e:
        print(e)
        return jsonify({"error_code": "AU-D-001", "error_message": "Unexpected error. Please try again."}), 400


@bp.route("/api/delete_user", methods=["POST"])
@roles_required("admin")
def delete_user():
    if not request.is_json:
        return jsonify({"error_code": "DU-R-001", "error_message": "Malformed request: Invalid JSON."}), 400

    request_data = request.get_json()
    user_id = request_data.get("user_id", None)

    if user_id is None:
        return jsonify({"error_code": "DU-U-001", "error_message": "Malformed request: User ID required."}), 400

    try:
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"deleted_user": user_id}), 200
        return jsonify({"error_code": "DU-U-002", "error_message": f"User {user_id} not found."}), 400
    except SQLAlchemyError as e:
        print(e)
        return jsonify({"error_code": "DU-D-001", "error_message": "Unexpected error. Please try again."}), 400
