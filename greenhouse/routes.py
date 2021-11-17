from flask import render_template, redirect, url_for, request, flash, make_response
from greenhouse.forms import RegistrationForm, LoginForm
import uuid
from greenhouse import db
from greenhouse import app
from greenhouse.models import users


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


# # http://localhost:5000/python/logout - this will be the logout page
# @app.route('/logout')
# def logout():
#     # Remove session data, this will log the user out
#     session.pop('loggedin', None)
#     session.pop('id', None)
#     session.pop('username', None)
#     # Redirect to login page
#     return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # generate ID for user
    users_id = uuid.uuid4()
    form = RegistrationForm(request.form)

    # Check the request method and validate the submit data
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        exists = db.session.query(
            db.session.query(users.username).filter_by(name=f'{username}').exists()
        ).scalar()
        if exists:
            return make_response(
                f'User with username: {username} already exists!'
            )
        else:
            new_user = users(
                user_id=users_id, username=form.username.data, name=form.name.data, location=form.location.data)
            new_user.password = form.password.data
            # Create an instance of the User class
            db.session.add(new_user)  # Adds new User record to database
            db.session.commit()  # Commits all changes

        flash('Thanks for registering')
        return redirect(url_for('dashboard'))
    else:
        return render_template('register.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('loginPage.html', form=form)

