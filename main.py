from flask import Flask, render_template, redirect, jsonify
from data.db_session import create_session, global_init
from data.recept import Recept
from data.users import User
from forms.register import RegisterForm
from forms.login import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


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


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.password.data != form.password_again.data:
        return render_template('register.html', title='Регистрация', form=form,
                               message="Пароли разные")
    db_sess = create_session()
    if db_sess.query(User).filter(User.login == form.login.data).first():
        return render_template('register.html', title='Регистрация', form=form,
                               message="This user already exists")
    user = User(
        name=form.name.data,
        login=form.login.data,
    )
    user.set_password(form.password.data)
    db_sess.add(user)
    db_sess.commit()
    return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('err404.html', title='Не найдено'), 404


@app.errorhandler(500)
def not_found_error(error):
    return render_template('err500.html', title='Внутренняя ошибка'), 500


def main():
    global_init('db/baze.db')
    app.run()


if __name__ == '__main__':
    main()
