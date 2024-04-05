from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user
from db.models import Apartment, User
from db.db import db_session
from config import csrf_token
from source.forms import LoginForm, RegistrationForm



app = Flask(__name__)
app.config['SECRET_KEY'] = csrf_token


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'  # Note: use the function name or endpoint

@login_manager.user_loader
def load_user(user_id):
    # Assuming you have a User model with a query attribute
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
            login_user(user)
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
    apartments = db_session.query(Apartment).all()
    apt_data = [
        {"photos": apt.photos,
         "addresses": apt.address,
         "rooms": apt.rooms,
         "area": apt.area,
         "city": apt.city
         }
        for apt in apartments
    ]
    apt_rooms = list(set(apt.rooms for apt in apartments))
    apt_areas = list(set(apt.area for apt in apartments))
    apt_cities = list(set(apt.city for apt in apartments))
    cities = set(apt['city'] for apt in apt_data)
    areas = set(apt['area'] for apt in apt_data)
    return render_template("index.html", apt_rooms=apt_rooms, cities=cities, apt_area=apt_areas,
                           apt_city=apt_cities, apt_data=apt_data, areas=areas)
@app.route('/filter', methods=['GET'])
def filter_apartments():
    selected_city = request.args.get('city', '')
    selected_area = request.args.get('area', '')

    apartments = db_session.query(Apartment).all()
    apt_data = [
        {"photos": apt.photos,
         "addresses": apt.address,
         "rooms": apt.rooms,
         "area": apt.area,
         "city": apt.city
         }
        for apt in apartments
    ]

    if selected_city:
        filtered_data = [apt for apt in apt_data if apt['city'] == selected_city]
    else:
        filtered_data = apt_data

    if selected_area:
        filtered_data = [apt for apt in apt_data if apt['area'] == selected_area]
    else:
        filtered_data = apt_data

    cities = set(apt['city'] for apt in apt_data)
    areas = set(apt['area'] for apt in apt_data)

    return render_template('index.html', cities=cities, areas=areas, apt_data=filtered_data)



@app.route("/add_new_review")
def add_review():
    if current_user.is_authenticated:
        return render_template("add_new_review.html")
    else:
        return redirect(url_for('main_page'))

@app.route("/apt_review_page")
def review_page():
    return render_template("apt_review_page.html")

if __name__ == "__main__":
    app.run(debug=True)

