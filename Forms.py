from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, DateField, TimeField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Пароль повторно', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class AddFilmForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    genre = StringField('Жанр', validators=[DataRequired()])
    director = StringField('Режиссер', validators=[DataRequired()])
    image = StringField('Ссылка на изображение', validators=[DataRequired()])
    date = StringField('Премьера')
    time = StringField('Продолжительность')
    description = TextAreaField('Описание')
    submit = SubmitField('Добавить')
