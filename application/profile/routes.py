# from flask import Blueprint, render_template, redirect, url_for, flash
# from application.profile.forms import SignUpForm, LoginForm
#
# profile_bp = Blueprint(
#     'profile_bp',__name__,
#     template_folder='templates',
#     static_folder='static'
# )
#
#
# @profile_bp.route("/register", methods=['GET', 'POST'])
# def register():
#     form = SignUpForm()
#     print(form.username.errors)
#     if form.validate_on_submit():
#         print(form.username.errors)
#         flash(f'Account created for {form.username.data}!', category="success")
#         actual_user = form.username.data
#
#         return redirect(url_for('home'))  # url_for wysyła do funkcji, a nie do html'a
#
#     return render_template("signup.html", form=form)
#
#
# @profile_bp.route("/login", methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         if form.email.data == 'admin@wp.pl' and form.password.data == 'password':
#             flash('You have been logged in', 'success')
#             return redirect(url_for('home'))
#         else:
#             flash('Login Unsuccesful', 'danger')
#
#     return render_template("login.html", form=form)