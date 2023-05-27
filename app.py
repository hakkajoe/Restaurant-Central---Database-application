from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from os import getenv
from sqlalchemy.sql import text
import secrets
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta


app = Flask(__name__)

import routes

