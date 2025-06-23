from flask_sqlalchemy import SQLAlchemy
from flask_security import Security

db = SQLAlchemy()
security = Security()

# Flask Security has strong opinions against password confirmation. This override re-enables it.
security.forms["confirm_register_form"].cls = security.forms["register_form"].cls
