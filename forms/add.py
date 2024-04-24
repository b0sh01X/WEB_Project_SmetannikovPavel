from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, SelectField
from wtforms.validators import DataRequired
from data import db_session
from data.catalog import Catalog


class AddForm(FlaskForm):
    db_session.global_init('db/base.db')
    db_sess = db_session.create_session()
    catalogs = db_sess.query(Catalog).all()
    name = StringField('Название рецепта', validators=[DataRequired()])
    text = TextAreaField('Рецепт', validators=[DataRequired()])
    reg = BooleanField('Доступно только для зарегистрированных пользователей', validators=[DataRequired()])
    catalog = SelectField('Выберете каталог', choices=[i.name for i in catalogs], validators=[DataRequired()])
    submit = SubmitField('Добавить рецепт')