from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    req = StringField('Поиск', validators=[DataRequired()])
    submit = SubmitField('Поиск')