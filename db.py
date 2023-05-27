from flask_sqlalchemy import SQLAlchemy
import psycopg2
from os import getenv
from app import app
from datetime import timedelta

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
db = SQLAlchemy(app)