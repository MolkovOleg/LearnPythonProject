from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user
from source.models import Apartment, Area, City, RoomCount, User
from source.db import db_session
from source.forms import LoginForm, RegistrationForm


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
            apartments = apartments.filter(RoomCount.rooms == selected_rooms)

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
        formа = RegistrationForm()
        return render_template('registration.html', forma=formа, title=title)

    @app.route('/process_reg', methods=['POST'])
    def process_reg():
        forma = RegistrationForm()
        if forma.validate_on_submit():
            new_user = User(
                email=forma.email.data,
                first_name=forma.first_name.data,
                last_name=forma.last_name.data,
                password=forma.password1.data,
                phone=forma.phone.data
            )
            new_user.set_password(forma.password1.data)
            db_session.add(new_user)
            db_session.commit()
            flash('Вы успешно зарегистрировались')
            return redirect(url_for('login_page'))
        else:
            for field, errors in forma.errors.items():
                for error in errors:
                    flash('Ошибка в поле "{}": - {}'.format(getattr(forma, field).label.text, error))
        return redirect(url_for('register'))

    @app.route("/login")
    def login_page():
        if current_user.is_authenticated:
            return redirect(url_for('main_page'))
        title = "Авторизация"
        forma = LoginForm()
        return render_template("auth.html", forma=forma, title=title)

    @app.route('/process_login', methods=['POST'])
    def process_login():
        forma = LoginForm()
        if forma.validate_on_submit():
            user = User.query.filter_by(email=forma.email.data).first()
            if user and user.check_password(forma.password.data):
                login_user(user)
                login_user(user, remember=forma.remember_me.data)

                flash('Вы вошли на сайт')
                return redirect(url_for('main_page'))

        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы вышли из аккаунта')
        return redirect(url_for('main_page'))

    @app.route("/apt_review_page", methods=['GET'])
    def review_page():
        apartments = db_session.query(Apartment).all()
        return render_template("apt_review_page.html", apartments=apartments)

    return app
