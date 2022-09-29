from flask import Flask, render_template
from random import choice

app = Flask(__name__)
title = ['flask', 'как интересно', 'ваше предложение', 'химия', '']
menu = [{'name': 'Главная', 'url': '/'}, {'name': 'Помощь', 'url': 'help'}, {'name': 'О приложении', 'url': 'about'}]


#добавил комментарий

@app.route('/index/')
@app.route('/')
def hello():
    user = {'usernames': 'yURA'}
    return render_template('index.html',  user=user, title=choice(title), menu=menu)
@app.route('/text/')
def text():
    return render_template('12.html', title = choice(title))



@app.route('/about/')
def about():
    return render_template('about.html', title = choice(title), menu=menu)

@app.route('/help/')
def help():
    return render_template('help.html', title = choice(title), menu=menu)

#динамичная страница
@app.route('/<name>')
def users(name):
    return render_template('nick.html', name=name, title = choice(title))

if __name__ == '__main__':
    app.run(debug=True)