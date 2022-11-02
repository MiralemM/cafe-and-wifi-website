from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from functools import wraps
from forms import CreateCafeForm, RegisterForm, LoginForm
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)


# Caffe TABLE Configuration
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))


class Cafe(db.Model):
    __tablename__ = "cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


with app.app_context():
    db.create_all()


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def home():
    cafes = Cafe.query.order_by(Cafe.id).all()
    db.session.commit()
    current_year = datetime.datetime.now().year
    return render_template("index.html", cafes=cafes, current_user=current_user, year=current_year)


@app.route("/cafe/<cafe_id>/", methods=["GET", "POST"])
def show_cafe(cafe_id):
    requested_cafe = Cafe.query.get(cafe_id)
    return render_template("cafe.html", cafe=requested_cafe, current_user=current_user)


@app.route("/suggest_places", methods=["GET", "POST"])
def suggest_places():
    form = CreateCafeForm()
    current_year = datetime.datetime.now().year
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            seats=form.seats.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            has_sockets=form.has_sockets.data,
            can_take_calls=form.can_take_calls.data,
            coffee_price=form.coffee_price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("suggest_places.html", form=form, current_user=current_user, year=current_year)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    current_year = datetime.datetime.now().year
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            print(User.query.filter_by(email=form.email.data).first())
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for("log_in"))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method="pbkdf2:sha256",
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for("home"))
    return render_template("register.html", form=form, current_user=current_user, year=current_year)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/log_in", methods=["GET", "POST"])
def log_in():
    form = LoginForm()
    current_year = datetime.datetime.now().year
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for("log_in"))
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for("log_in"))
        else:
            login_user(user)
            return redirect(url_for("home"))
    return render_template("log_in.html", form=form, current_user=current_user, year=current_year)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/delete/<int:cafe_id>")
@admin_only
def delete_cafe(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
