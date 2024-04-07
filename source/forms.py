from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo,
                                Length, ValidationError)
from db.models import User


class LoginForm(FlaskForm):
    email = StringField('Имя пользователя', validators=[DataRequired()],
                        render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    submit = SubmitField('Sign in',
                         render_kw={"class":
                                    "btn btn-lg btn-primary btn-block-*"})


class RegistrationForm(FlaskForm):
    first_name = StringField('Имя пользователя',
                             validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    last_name = StringField('Фамилия пользователя',
                            validators=[DataRequired()],
                            render_kw={"class": "form-control"})
    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={"class": "form-control"})
    phone = StringField("Телефон",
                        validators=[DataRequired(), Length(min=11)],
                        render_kw={"class": "form-control"})
    password = PasswordField('Пароль',
                             validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    password2 = PasswordField('Повторите пароль',
                              validators=[DataRequired(), EqualTo('password')],
                              render_kw={"class": "form-control"})
    submit = SubmitField('Зарегистрироваться',
                         render_kw={"class":
                                    "btn btn-lg btn-primary "
                                    "btn-block btn-outline-*"})

    def validate_email(self, email):
        users_count = User.query.filter_by(email=email.data).count()
        if users_count > 0:
            raise ValidationError(
                'Пользователь с такой электронной почтой уже зарегистрирован'
            )

    def validate_phone(self, phone):
        users_phone_count = User.query.filter_by(phone=phone.data).count()
        if users_phone_count > 0:
            raise ValidationError(
                'Пользователь с таким телефоном уже зарегистрирован'
            )
