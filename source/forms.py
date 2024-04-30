from flask_wtf import FlaskForm
from wtforms import (BooleanField, PasswordField, StringField,
                     SubmitField, TextAreaField, IntegerField,
                     MultipleFileField, URLField, FileField)
from wtforms.validators import (DataRequired, Email, EqualTo,
                                NumberRange, Length, ValidationError)
from source.db.models import User


class LoginForm(FlaskForm):
    email = StringField('Имя пользователя', validators=[DataRequired()],
                        render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    submit = SubmitField('Войти',
                         render_kw={"class": "btn",
                                    "style": "background-color: #ADD8E6;"})
    remember_me = BooleanField('Запомнить меня',
                               default=True,
                               render_kw={"class": "form-check-input"})


class RegistrationForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    last_name = StringField('Фамилия', validators=[DataRequired()],
                            render_kw={"class": "form-control"})
    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={"class": "form-control"})
    phone = StringField('Телефон', validators=[DataRequired(), Length(min=11)],
                        render_kw={"class": "form-control"})
    password1 = PasswordField('Пароль', validators=[DataRequired()],
                              render_kw={"class": "form-control"})
    password2 = PasswordField('Повторите пароль',
                              validators=[DataRequired(),
                                          EqualTo('password1')],
                              render_kw={"class": "form-control"})
    submit = SubmitField('Зарегистрироваться',
                         render_kw={"class": "btn", "style":
                                    "background-color: #ADD8E6;"})

    def validate_email(self, email):
        users_count = User.query.filter_by(email=email.data).count()
        if users_count:
            raise ValidationError('Пользователь с такой '
                                  'электронной почтой уже зарегистрирован')

    def validate_phone(self, phone):
        users_phone_count = User.query.filter_by(phone=phone.data).count()
        if users_phone_count:
            raise ValidationError('Пользователь с таким '
                                  'телефоном уже зарегистрирован')


class FeedbackForm(FlaskForm):
    apartment_id = IntegerField('Введите id квартира',
                                validators=[DataRequired()],
                                render_kw={"class": "form-control"})
    raiting = IntegerField('Rating', validators=[DataRequired(),
                                                 NumberRange(min=0, max=10)],
                           render_kw={"class": "form-control"})
    price = IntegerField('Price', validators=[DataRequired()],
                         render_kw={"class": "form-control"})
    text = TextAreaField('Введите отзыв', validators=[DataRequired()],
                         render_kw={"class": "form-control"})
    photo = MultipleFileField('Загрузите фото',
                              render_kw={"class": "form-control-file"})
    user_id = IntegerField(validators=[DataRequired()])
    submit = SubmitField('Оставить отзыв',
                         render_kw={"class": "btn btn-lg btn-primary "
                                             "btn-block btn-outline-*"})


class ApartmentForm(FlaskForm):
    owner_name = StringField('Введите имя арендатора',
                             validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    city = StringField('Город', validators=[DataRequired()],
                       render_kw={"class": "form-control"})
    area = StringField('Район', validators=[DataRequired()],
                       render_kw={"class": "form-control"})
    address = StringField('Улица', validators=[DataRequired()],
                          render_kw={"class": "form-control"})
    bld = IntegerField('Дом', validators=[DataRequired()],
                       render_kw={"class": "form-control"})
    apt = IntegerField('Квартира', validators=[DataRequired()],
                       render_kw={"class": "form-control"})
    rooms = IntegerField('Количество комнат', validators=[DataRequired()],
                         render_kw={"class": "form-control"})
    price = IntegerField('Price', validators=[DataRequired()],
                         render_kw={"class": "form-control"})
    url = URLField('Введите ссылку', render_kw={"class": "form-control"})
    photo = FileField('Загрузите фото',
                      render_kw={"class": "form-control-file"})
    submit = SubmitField('Создать квартиру',
                         render_kw={"class": "btn btn-lg "
                                    "btn-primary btn-block btn-outline-*"})
