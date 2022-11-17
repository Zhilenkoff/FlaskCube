import sqlite3


from app import connect_db, app


def create_db():
    '''Вспомогательная функция для создания таблиц БД'''
    db = connect_db()
    with app.open_resource('sql_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


if __name__ == '__main__':
    db = connect_db()
    dbase = FlaskDataBase(db)
    print(dbase.addmenu('О нас', '/about'))
    print(dbase.addmenu('Помощь', '/help'))
    #print(dbase.dellmenu())
    print(create_db.__doc__)

