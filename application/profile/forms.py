from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, length, Email, EqualTo, regexp


class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email(message="Enter a valid email")])
    password = PasswordField('Password (5)',
                             validators=[DataRequired(), length(min=5, message="Select a stronger password"),
                                         regexp("^(?=.*[0-9]+.*)(?=.*[a-zA-Z]+.*)[0-9a-zA-Z]{6,}$")])
    confirm_password = PasswordField('Confirm_Password',
                                     validators=[DataRequired(), length(min=5),
                                                 EqualTo('password', message="Passwoerd must match")])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email(message='Enter a valid email.')])
    password = PasswordField('Password',
                             validators=[DataRequired(), length(min=5)])
    submit = SubmitField('Login')


class gu(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


# class SignUpForm(FlaskForm):
#     username = StringField("Username", validators=[DataRequired(), length(min=2, max=20)])
#     email = StringField("Email", validators=[DataRequired(), Email(message="Enter a valid email")])
#     password = PasswordField('Password (5)',
#                              validators=[DataRequired(), length(min=5, message="Select a stronger password"),
#                              regexp("^(?=.*[0-9]+.*)(?=.*[a-zA-Z]+.*)[0-9a-zA-Z]{6,}$")])
#     confirm_password = PasswordField('Confirm_Password',
#                                      validators=[DataRequired(), length(min=5),
#                                                  EqualTo('password', message="Passwoerd must match")])
#     submit = SubmitField('Sign Up')

