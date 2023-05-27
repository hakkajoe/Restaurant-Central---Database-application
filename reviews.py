from db import db
from sqlalchemy.sql import text

def reviews_for_index():
    sql = text("SELECT stars, restaurant_id FROM reviews")
    result = db.session.execute(sql)
    reviews = result.fetchall()
    return reviews

def reviews_for_restaurant(id):
    sql = text("SELECT id, reviewer, stars, textreview, date, restaurant_id FROM reviews WHERE restaurant_id=:id")
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def new(restaurant_id, stars, textreview, reviewer):
    sql = text("INSERT INTO reviews (reviewer, stars, textreview, date, restaurant_id) VALUES (:reviewer, :stars, :textreview, NOW(), :restaurant_id)")
    db.session.execute(sql, {"reviewer":reviewer, "stars":stars, "textreview":textreview, "restaurant_id":restaurant_id})
    db.session.commit()

def delete(id):
    sql = text("DELETE FROM reviews WHERE id=:id RETURNING restaurant_id")
    result = db.session.execute(sql, {"id":id})
    db.session.commit()
    return result.fetchone()[0]