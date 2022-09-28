from flask import Flask, render_template

app = Flask(__name__)
#добавил комментарий
@app.route('/')
@app.route('/tex/')
def text():
    return render_template('12.html')

@app.route('/hello/')
def hello():
    return render_template('index.html')

#динамичная страница
@app.route('/<name>')
def users(name):
    return render_template('nick.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)