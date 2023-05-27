from db import db
from sqlalchemy.sql import text


def get_all():
    sql = text("SELECT id, name FROM classes")
    result = db.session.execute(sql)
    classes = result.fetchall()
    return classes

def delete(deletions):
    for delete in deletions:
        sql = text("DELETE FROM classes WHERE id=:id")
        db.session.execute(sql, {"id": delete})
    db.session.commit()

def insert(answers):
    for answer in answers:
        if answer != "":
            sql = text("INSERT INTO classes (name) VALUES (:answer)")
            db.session.execute(sql, {"answer":answer})
    db.session.commit()