from flask import Flask, render_template, redirect, jsonify
from flask_login import current_user, login_required, logout_user, login_user, LoginManager
from data.db_session import create_session, global_init
from data.recept import Recept
from data.users import User
from data.catalog import Catalog
from forms.add import AddForm
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.search import SearchForm

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
@app.route('/main/')
def index():
    return redirect('/main/new')


@app.route('/main/<s>')
def glav(s):
    db_sess = create_session()
    request = db_sess.query(Recept).all()
    req = []
    for i in request:
        db_sess = create_session()
        user = db_sess.query(User).filter(User.id == i.autor).first()
        i.autor = user.name
        req.append(i)
    if s == 'old':
        sorti = 'Более старые'
    elif s == 'new':
        sorti = 'Более новые'
        request.reverse()
    else:
        return '<h1>Неверная сортировка<h1>', 404
    return render_template('main.html', title='Главная страница', sorti=sorti, request=req)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли разные")
        db_sess = create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пользователь уже зарегистрирован")
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
        return render_template('login.html', title='Авторизация', message='Неправильный логин или пароль', form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(f'/search/{form.req.data}')
    return render_template('search.html', title='Поиск', form=form)


@app.route('/search/<s>')
def search1(s):
    db_sess = create_session()
    recept = db_sess.query(Recept).all()
    sp = []
    for i in recept:
        if s in i.name or s in i.text:
            sp.append(i)
    req = []
    for i in sp:
        db_sess = create_session()
        user = db_sess.query(User).filter(User.id == i.autor).first()
        i.autor = user.name
        req.append(i)
    return render_template('search1.html', title=f'Результаты поиска - {len(req)} результатов', sp=req)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddForm()
    if form.validate_on_submit():
        db_sess = create_session()
        recept = Recept(name=form.name.data,
                        text=form.text.data,
                        reg=form.reg.data)
        recept.autor = current_user.id
        print(form.catalog, form.name, form.text)
        recept.catalog_id = db_sess.query(Catalog).filter(Catalog.name == form.catalog.data).first().id
        db_sess.add(recept)
        db_sess.commit()
        return redirect('/')
    return render_template('add.html', title='Добавление рецепта', form=form)


@app.route('/catalog')
def catalog():
    db_sess = create_session()
    request = db_sess.query(Catalog).all()
    return render_template('catalog.html', title='Каталог', request=request)


@app.route('/catalog/<s>')
def catalog1(s):
    db_sess = create_session()
    catalog = db_sess.query(Catalog).filter(Catalog.link == s).first()
    if catalog:
        sp = db_sess.query(Recept).filter(Recept.catalog_id == catalog.id).all()
        req = []
        for i in sp:
            db_sess = create_session()
            user = db_sess.query(User).filter(User.id == i.autor).first()
            i.autor = user.name
            req.append(i)
        return render_template('catalog1.html', title='Список блюд', req=req)
    return '<h1>Список не найден</h1>', 404


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
