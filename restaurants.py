from sqlalchemy.sql import text
from db import db

def restaurants_for_index():
    sql = text("SELECT id, name, description FROM restaurants ORDER BY name")
    result = db.session.execute(sql)
    restaurants = result.fetchall()
    return restaurants

def search(query):
    sql = text("SELECT id, name, description FROM restaurants WHERE name LIKE :query OR description LIKE :query")
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    matches = result.fetchall()
    return matches

def new(name, description):
    sql = text("INSERT INTO restaurants (name, description) VALUES (:name, :description) RETURNING id")
    result = db.session.execute(sql, {"name":name, "description":description})
    db.session.commit()
    return result.fetchone()[0]

def restaurant_edit(id):
    sql = text("SELECT * FROM restaurants WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def update(name, description, restaurant_id):
    sql = text("UPDATE restaurants SET name=:name, description=:description WHERE id=:restaurant_id RETURNING id")
    result = db.session.execute(sql, {"name":name, "description":description, "restaurant_id": restaurant_id})
    db.session.commit()
    return result.fetchone()[0]

def for_review(id):
    sql = text("SELECT id, name FROM restaurants WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[1]

def delete(id):
    sql = text("DELETE FROM restaurants WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()