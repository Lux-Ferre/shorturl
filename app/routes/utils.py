from flask import g
from flask_security import current_user


def register_hooks(app):
	@app.before_request
	def set_logged_in_flag():
		g.logged_in = current_user.is_authenticated

	@app.before_request
	def set_is_admin_flag():
		g.is_admin = current_user.has_role("admin") if current_user.is_authenticated else False

	@app.context_processor
	def inject_logged_in():
		return {"logged_in": getattr(g, "logged_in", False)}

	@app.context_processor
	def inject_is_admin():
		return {"is_admin": getattr(g, "is_admin", False)}
