from db import db
from sqlalchemy.sql import text

def get_all():
    sql = text("SELECT id, restaurant_id, class_id FROM restaurant_classes")
    result = db.session.execute(sql)
    restaurant_classes = result.fetchall()
    return restaurant_classes

def insert(restaurant_id, tags):
    for class_id in tags:
        if class_id:
            sql = text("INSERT INTO restaurant_classes (restaurant_id, class_id) VALUES (:restaurant_id, :class_id)")
            db.session.execute(sql, {"restaurant_id":restaurant_id, "class_id":class_id})
    db.session.commit()

def for_editing(id):
    sql = text("SELECT * FROM restaurant_classes WHERE restaurant_id=:id")
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def delete(restaurant_id):
    sql = text("DELETE FROM restaurant_classes WHERE restaurant_id=:restaurant_id")
    db.session.execute(sql, {"restaurant_id":restaurant_id})
    db.session.commit()