import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECURITY_MSG_DISABLED_ACCOUNT = ("Your account is pending approval.", "error")
    SECURITY_MSG_CONFIRMATION_REQUIRED = ("Your account is pending approval.", "error")
    SECURITY_MSG_CONFIRM_REGISTRATION = ("Your account is pending approval.", "error")

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SECURITY_REGISTERABLE = os.environ.get("SECURITY_REGISTERABLE") == "True"
    SECURITY_CONFIRMABLE = os.environ.get("SECURITY_CONFIRMABLE") == "True"
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")
    SECURITY_PASSWORD_HASH = os.environ.get("SECURITY_PASSWORD_HASH")
    SECURITY_SEND_REGISTER_EMAIL = os.environ.get("SECURITY_SEND_REGISTER_EMAIL") == "True"
    DEFAULT_ADMIN_EMAIL = os.environ.get("DEFAULT_ADMIN_EMAIL")
    DEFAULT_ADMIN_PASSWORD = os.environ.get("DEFAULT_ADMIN_PASSWORD")
