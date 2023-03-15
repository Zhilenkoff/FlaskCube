import sqlite3

from app import connect_db, app
from flask_db_class import FlaskDataBase


def create_db():
    ''' Вспомогательная функция для создания таблиц БД'''
    db = connect_db()
    with app.open_resource('sql_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()
    pass





if __name__ == '__main__':
     db = connect_db()
     dbase = FlaskDataBase(db)
     a = dbase.getPost("tashkent_test")
     text = a[1].replace("./", "/static/images_html/", a[1].count("./"))
     dbase.dellPost(3)

     dbase.addPost("tashkent", text, "tashkent")
