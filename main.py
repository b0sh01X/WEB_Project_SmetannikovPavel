from flask import Flask, render_template, redirect, jsonify
from flask_login import current_user, login_required, logout_user, login_user, LoginManager
from data.db_session import create_session, global_init
from data.recept import Recept
from data.users import User
from forms.register import RegisterForm
from forms.login import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/main')
def index():
    return redirect('/main/new')


@app.route('/main/<s>')
def glav(s):
    db_sess = create_session()
    request = db_sess.query(Recept).all()
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect('/')
        return render_template('login.html', message='Неправильный логин или пароль', form=form)
    return render_template('login.html', form=form)



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
