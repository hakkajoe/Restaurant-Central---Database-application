from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

def check(username):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    return user

def create(username, password):
    hash_value = generate_password_hash(password)
    sql = text("INSERT INTO users (username, password, admin) VALUES (:username, :password, 'no')")
    db.session.execute(sql, {"username":username, "password":hash_value, "admin": 'no'})
    db.session.commit()