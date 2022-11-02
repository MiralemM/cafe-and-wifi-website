from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, URL


class CreateCafeForm(FlaskForm):
    name = StringField("Name of the Coffee Shop", validators=[DataRequired()])
    map_url = StringField("Enter an URL location", validators=[DataRequired(), URL()])
    img_url = StringField("New Cafe Image URL", validators=[DataRequired(), URL()])
    location = StringField("Enter Address of the new cafe", validators=[DataRequired()])
    has_sockets = BooleanField("Does It Have Sockets?", default=False)
    has_toilet = BooleanField("Does It Have Toilet?", default=False)
    has_wifi = BooleanField("Does It Have Wi-Fi?", default=False)
    can_take_calls = BooleanField("Can you take calls in object?", default=False)
    seats = SelectField("How many seats are in object?", validators=[DataRequired()],
                        choices=["0-10", "10-20", "20-30", "30-40", "40-50", "50+"])
    coffee_price = StringField("Enter Coffee Price", validators=[DataRequired()])
    submit = SubmitField("Submit New Cafe")


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")
