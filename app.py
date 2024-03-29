#C:\Users\r1212\AppData\Local\Yandex\YandexBrowser\User Data\Default\Network
import datetime
import sqlite3

from flask import Flask, render_template, session, redirect, url_for, request, abort, g, flash
from random import choice

from config import Config
import os
#import git

from flask_db_class import FlaskDataBase

app = Flask(__name__)

# app.config['SECRET_KEY'] = 'dhme;kghjanrkael/jgbuilarelkjmgbipuehjmghiotrkjhtoikle'
app.config.from_object(Config)
# print(*app.config.items(), sep='\n')
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flask.db')))
# print(*app.config.items(), sep='\n')
title = ['Flask', 'Как интересно', 'Ваши предложения', 'Химия', '']
menu = [{'name': 'Главная', 'url': '/'}, {'name': 'Помощь', 'url': 'help'}, {'name': 'О приложении', 'url': 'about'},
        {'name': 'Таблица', 'url': 'table'}, {'name': 'Авторизация', 'url': 'login'},
        {'name': 'Главная БД', 'url': '/db/index_db'}]

#@app.route('/update_server', methods=['POST'])
#def webhook():
    #if request.method == 'POST':
        #repo = git.Repo('/home/Michael12211/flaskCUB')
        #origin = repo.remotes.origin
        #origin.pull()
        #return 'Updated PythonAnywhere successfully', 200
    #else:
        #return 'Wrong event type', 400

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    '''соединение с БД, если оно еще не установленно'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    ''' закрываем соединение с БД'''
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route("/test")
def test():
    content = render_template("index.html", session=session, menu=menu)
    res = make_response(content)
    res.headers["Content-Type"] = "multipad/from"


@app.route('/db/index_db')
def index_db():
    db = get_db()
    db = FlaskDataBase(db)
    return render_template('index_db.html', menu=db.getmenu(), posts=db.getPosts())


@app.route('/db/<alias>')
def showPost(alias):
    db = get_db()
    db = FlaskDataBase(db)
    title, post = db.getPost(alias)
    if not title:
        abort(404)
    return render_template('post.html', menu=db.getmenu(), title=title, post=post)


@app.route('/db/add-post', methods=['POST', 'GET'])
def add_post():
    db = get_db()
    db = FlaskDataBase(db)
    if request.method == 'POST':
        if len(request.form['name']) > 3 and 10 < len(request.form['post']) < 2 ** 20:
            res = db.addPost(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья добавлена', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')

    return render_template('addpost.html', menu=db.getmenu())


@app.route('/index/')
@app.route('/')
def hello():
    user = {'username': 'user'}
    return render_template('index.html', user=user, title=choice(title), menu=menu)


@app.route('/help')
def help():
    return render_template('help.html', title='Помощь', menu=menu)


@app.route('/about')
def about():
    return render_template('about.html', title='IT CUB', menu=menu)


# @app.route('/<int:id>')
# def users(id):
#     return f'<h1>Ваш порядковый номер {id} </h1>'


@app.route('/profile/<user>')
def profile(user):
    if 'user_logged' not in session or session['user_logged'] != user:
        abort(401)


    return render_template('nick.html', name=user, menu=menu)


# @app.route('/profile/<username>')
# def profile(username):
#     return f'hello {username}'


@app.route('/table')
def t1():
    return render_template('table.html', menu=menu)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Страница не найдена', menu=menu)


@app.errorhandler(401)
def profile_error(error):
    return f"<h1> Сперва авторизуйтесь </h1> {error}"


app.permanent_session_lifetime = datetime.timedelta(seconds=160)


@app.route('/login', methods=["POST", "GET"])
def login():
    print(session)
    users ={'Максим': '123123', 'Дима':'159753', 'Настя':'18012007'}

    if 'user_logged' in session:
        print(session['user_logged'])
        return redirect(url_for('profile', user=session['user_logged']))
    elif request.method == 'POST' and request.form['username'] in users and request.form[
        'password'] in users[request.form['username']]:  # and request.method == 'GET':
        session['user_logged'] = request.form['username']
        return redirect(url_for('profile', user=session['user_logged']))
    return render_template('login.html', title="Авторизация", menu=menu)


@app.route('/visits-counter')
def visits():
    session.permanent = True
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1  # чтение и обновление данных сессии
    else:
        session['visits'] = 1  # настройка данных сессии
    return "Total visits: {}".format(session.get('visits'))


@app.route('/delete-visits')
def delete_visits():
    session.pop('visits', None)  # удаление данных о посещениях
    return 'Visits deleted'

@app.route('/delete_exit')
def delete_exit():
    if session.get('user_logged', False):
        del session['user_logged']
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)