import os
from dotenv import load_dotenv, dotenv_values

# load from .env
load_dotenv()


# Create a class of imported constants from .env file
class Config:
    UCONRA_DATABASE_URI = os.getenv('UCONRA_DATABASE_URI')
    SQLALCHEMY_BINDS_KEY = os.getenv('Employee_roles')
    SQLALCHEMY_BINDS_URL = os.getenv('mysql+pymysql://root:root@localhost/Fruutty_employees')
    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    GOOGLE_RECAPTCHA_SITE_KEY = os.getenv('GOOGLE_RECAPTCHA_SITE_KEY')
    GOOGLE_RECAPTCHA_SECRETE_KEY = os.getenv('GOOGLE_RECAPTCHA_SECRETE_KEY')
    GOOGLE_RECAPTCHA_VERIFY_URL = os.getenv('GOOGLE_RECAPTCHA_VERIFY_URL')
    UCONRA_EMAIL = os.getenv('UCONRA_EMAIL')
    SMTP_EMAIL_SERVER = os.getenv('SMTP_EMAIL_SERVER')
    SERVER_EHLO = os.getenv('SERVER_EHLO')
    APP_PASSWORD = os.getenv('APP_PASSWORD')
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')
    BASE_TOKEN = os.getenv('BASE_TOKEN')
    TOKEN_ID = os.getenv('TOKEN_ID')
    ADMIN = os.getenv('ADMIN')