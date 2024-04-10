from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user

from db.models import Apartment, User, City, Area, RoomCount, Feedback
from db.db import db_session
from config import csrf_token
from source.forms import LoginForm, RegistrationForm, FeedbackForm


app = Flask(__name__)
app.config['SECRET_KEY'] = csrf_token


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'


@login_manager.user_loader
def load_user(user_id):
    return db_session.query(User).get(int(user_id))


@app.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))
    title = "Регистрация"
    form = RegistrationForm()
    return render_template('registration.html', forma=form, title=title)


@app.route('/process-reg', methods=['POST'])
def process_reg():
    forma = RegistrationForm()
    if forma.validate_on_submit():
        new_user = User(email=forma.email.data,
                        first_name=forma.first_name.data,
                        last_name=forma.last_name.data,
                        password=forma.password.data,
                        phone=forma.phone.data
                        )
        new_user.set_password(forma.password.data)
        db_session.add(new_user)
        db_session.commit()
        return redirect(url_for('login_page'))
    else:
        for field, errors in forma.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": - {}'.format(
                    getattr(forma, field).label.text,
                    error
                ))
    return redirect(url_for('register'))


@app.route("/login")
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))
    title = "Авторизация"
    form = LoginForm()
    return render_template("auth.html", form=form, title=title)


@app.route('/login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы вошли на сайт')
            return redirect(url_for('main_page'))
    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('process_login'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_page'))


@app.route("/")
def main_page():
    city_select = db_session.query(City).all()
    area_select = db_session.query(Area).all()
    room_count_select = db_session.query(RoomCount).all()
    apartments = db_session.query(Apartment).all()
    return render_template("index.html", apartments=apartments,
                           city_select=city_select, area_select=area_select, room_count_select=room_count_select)


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

    return render_template("index.html", apartments=apartments.all(),
                           city_select=city_select, area_select=area_select, room_count_select=room_count_select)


@app.route("/add_new_review", methods=['GET', 'POST'])
def add_new_review():
    title = 'Оставьте отзыв'
    apartments = db_session.query(Apartment)
    form = FeedbackForm()
    if current_user.is_authenticated:
        return render_template("add_new_review.html", form=form, title=title, apartments=apartments)
    else:
        return redirect(url_for('main_page'))


@app.route("/create_feedback", methods=['POST'])
def create_feedback():
    selected_apt = request.args.get('', '')
    print(f'dfsd{selected_apt}')
    selected_apt_id = db_session.query(Apartment).filter(Apartment.address == selected_apt)
    print(selected_apt_id.all())
    form = FeedbackForm()
    if current_user.is_authenticated:
        new_feedback = Feedback(apartment_id=selected_apt_id,
                                raiting=form.raiting.data,
                                price=form.price.data,
                                owner_name=form.owner_name.data,
                                text=form.text.data,
                                photo=form.photo.data
                                )
        db_session.add(new_feedback)
        db_session.commit()
        return redirect(url_for('main_page'))
    else:
        return redirect(url_for('main_page'))


@app.route("/apt_review_page")
def review_page():
    return render_template("apt_review_page.html")


if __name__ == "__main__":
    app.run(debug=True)
