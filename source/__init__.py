import datetime

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user

from source.db.models import Apartment, Area, City, Feedback, RoomCount, User, FeedbackUser
from source.db.db import db_session
from source.forms import LoginForm, RegistrationForm, FeedbackForm


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.secret_key = app.config['SECRET_KEY']

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login_page'

    @login_manager.user_loader
    def load_user(user_id):
        return db_session.query(User).get(user_id)

    @app.route("/")
    def main_page():
        city_select = db_session.query(City).all()
        area_select = db_session.query(Area).all()
        room_count_select = db_session.query(RoomCount).all()
        apartments = db_session.query(Apartment).all()

        return render_template("index.html",
                               apartments=apartments,
                               city_select=city_select,
                               area_select=area_select,
                               room_count_select=room_count_select)

    @app.route('/filter', methods=['GET'])
    def filter_apartments():
        city_select = db_session.query(City).all()
        area_select = db_session.query(Area).all()
        room_count_select = db_session.query(RoomCount).all()
        selected_city = request.args.get('city', '')
        selected_area = request.args.get('area', '')
        selected_rooms = request.args.get('room', '')

        apartments = (db_session.query(Apartment).join(City).join(Area).join(RoomCount))

        if selected_city:
            apartments = apartments.filter(City.name == selected_city)

        if selected_area:
            apartments = apartments.filter(Area.name == selected_area)

        if selected_rooms:
            apartments = apartments.filter(RoomCount.name == selected_rooms)

        return render_template("index.html",
                               apartments=apartments.all(),
                               city_select=city_select,
                               area_select=area_select,
                               room_count_select=room_count_select)

    @app.route('/register')
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('main_page'))
        title = "Регистрация"
        form = RegistrationForm()
        return render_template('registration.html', form=form, title=title)

    @app.route('/process_reg', methods=['POST'])
    def process_reg():
        form = RegistrationForm()
        if form.validate_on_submit():
            new_user = User(
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                password=form.password1.data,
                phone=form.phone.data
            )
            new_user.set_password(form.password1.data)
            db_session.add(new_user)
            db_session.commit()
            flash('Вы успешно зарегистрировались')
            return redirect(url_for('login_page'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash('Ошибка в поле "{}": - {}'.format(getattr(form, field).label.text, error))
        return redirect(url_for('register'))

    @app.route("/login")
    def login_page():
        if current_user.is_authenticated:
            return redirect(url_for('main_page'))
        title = "Авторизация"
        form = LoginForm()
        return render_template("auth.html", form=form, title=title)

    @app.route('/process_login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                login_user(user, remember=form.remember_me.data)

                flash('Вы вошли на сайт')
                return redirect(url_for('main_page'))

        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы вышли из аккаунта')
        return redirect(url_for('main_page'))

    @app.route("/add_new_review", methods=['GET', 'POST'])
    def add_new_review():
        title = 'Оставьте отзыв'
        apartments = db_session.query(Apartment)
        form = FeedbackForm()
        if current_user.is_authenticated:
            return render_template("add_new_review.html", form=form, title=title, apartments=apartments)
        else:
            flash('Вы неавторизованы')
            return redirect(url_for('login_page'))

    @app.route("/create_feedback", methods=['POST'])
    def create_feedback():
        selected_apt = request.form.get('apt')
        selected_apt_id = db_session.query(Apartment).filter(Apartment.address == selected_apt).first()
        form = FeedbackForm()
        if current_user.is_authenticated:
            new_feedback = Feedback(apartment_id=selected_apt_id.id,
                                    raiting=form.raiting.data,
                                    price=form.price.data,
                                    owner_name=selected_apt_id.owner_name,
                                    text=form.text.data,
                                    photo=form.photo.data,
                                    )
            db_session.add(new_feedback)
            db_session.commit()
            new_feedback_id = FeedbackUser(user_id=current_user.get_id(),
                                           feedback_id=new_feedback.id,
                                           publication_date=datetime.datetime.now()
                                           )
            db_session.add(new_feedback_id)
            db_session.commit()
            return redirect(url_for('main_page'))
        else:
            flash('Вы неавторизованы')
            return redirect(url_for('login_page'))

    @app.route("/apt_review_page", methods=['GET'])
    def review_page():
        apartments = db_session.query(Apartment).all()
        return render_template("apt_review_page.html", apartments=apartments)

    @app.route("/profile")
    def profile():
        title = "Профиль"
        personal_info = "Личная информация"
        reviews = "Ваши отзывы"
        user_info = db_session.query(User).filter(User.id == current_user.get_id())
        if current_user.is_authenticated:
            user_feedback = ((db_session.query(Feedback)
                             .join(FeedbackUser, Feedback.id == FeedbackUser.feedback_id)
                             .join(Apartment, Apartment.id == Feedback.apartment_id)
                             .filter(FeedbackUser.feedback_id == Feedback.id))
                             .all())
            return render_template("profile.html", user_feedback=user_feedback, title=title,
                                   reviews=reviews, user_info=user_info, personal_info=personal_info)
        else:
            flash('Вы неавторизованы')
            return redirect(url_for('login_page'))

    return app
