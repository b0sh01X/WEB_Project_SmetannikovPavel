from flask import Flask, render_template, redirect, jsonify
import sqlite3

app = Flask(__name__)


@app.route('/')
@app.route('/main')
def index():
    return redirect('/main/new')


@app.route('/main/<s>')
def glav(s):
    bd = sqlite3.connect('db/baze.db')
    request = bd.cursor().execute('SELECT * FROM recept').fetchall()
    bd.close()
    if s == 'old':
        sorti = 'Более старые'
    elif s == 'new':
        sorti = 'Более новые'
        request.reverse()
    else:
        return '<h1>Неверная сортировка<h1>', 404
    return render_template('main.html', title='Главная страница', sorti=sorti, request=request)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('err404.html', title='Не найдено'), 404


@app.errorhandler(500)
def not_found_error(error):
    return render_template('err500.html', title='Внутренняя ошибка'), 500


def main():
    app.run()


if __name__ == '__main__':
    main()
