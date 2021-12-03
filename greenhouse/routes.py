from flask import render_template, redirect, url_for, request, flash, make_response, session
from greenhouse.forms import RegistrationForm, LoginForm, plantForm
import uuid
from greenhouse import db, bcrypt, app, logger
from greenhouse.models import users as User, plant_readings,user_plant
from flask_login import login_user, current_user, logout_user, login_required
import json
from types import SimpleNamespace



@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


alive = 0
data = {}


@app.route('/register', methods=['GET', 'POST'])
def register():
    # generate ID for user
    users_id = uuid.uuid4().int
    login_form = LoginForm()
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('myPlants'))
    # Check the request method and validate the submit data
    if request.method == 'POST' and form.validate_on_submit():
        new_user = User(
            user_id=users_id,
            username=form.username.data,
            name=form.name.data, )
        password = form.password.data
        new_user.password = User.hash(password)
        # Create an instance of the User class
        db.session.add(new_user)  # Adds new User record to database
        db.session.commit()  # Commits all changes
        return redirect(url_for('loginPage2'))
    return render_template('loginPage2.html', loginForm=login_form, registerForm=form )


@app.route('/login', methods=['GET', 'POST'])
def login():

    register_form = RegistrationForm()
    login_form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):

            login_user(user)
            session['password'] = user.password

            return redirect(url_for("index"))
        else:
            flash('login unsuccessful check username and password')
    return render_template('loginPage2.html',loginForm=login_form, registerForm=register_form )


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for("loginPage2"))

@app.route('/account', methods=['GET', 'POST'])
def account():
    return render_template('account.html')

@app.route("/", methods=['GET', 'POST'])
def loginPage2():
    register_form = RegistrationForm()
    login_form = LoginForm()
    return render_template("loginPage2.html", loginForm=login_form, registerForm=register_form)


@app.route("/updateStats", methods=['GET', "POST"])
def updateStats():
    data = request.data
    plant = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    try:
        dbplant = plant_readings.query.filter_by(user_id=plant.user_id).first()
        print(dbplant)
        if request.method == 'POST':
            readings = plant_readings(
                user_id=dbplant.user_id,
                raspi_id=dbplant.user_id,
                plant_id=plant.plant_id,
                temperature=plant.temperature,
                humidity=plant.humidity,
                soil_moisture=plant.soil_moisture,
            )
            db.session.add(readings)
            db.session.commit()
    except RuntimeError as error:
        raise RuntimeError('specific message') from error

    return render_template("myPlants.html", data=data)

@app.route("/custom", methods=['GET', 'POST'])
@login_required
def custom():

    pw = session.get('password')
    user = User.query.filter_by(password=pw).first()
    form = plantForm(request.form)
    if user:
        if request.method == 'POST' and form.validate_on_submit():
            new_plant = user_plant(
                user_id=user.user_id,
                plant_name=form.plant_name.data,
                plant_id=form.plant_id.data,
                planted=form.date_planted.data,
            )
            # Create an instance of the plant class
            db.session.add(new_plant)  # Adds new User record to database
            db.session.commit()  # Commits all changes
            return redirect(url_for('myPlants'))

    return render_template("custom.html", form=form)


@app.route("/index")
def index():
    return render_template("index.html")


@app.route('/myPlants')
@login_required
def myPlants():

    pw = session.get('password')
    user = User.query.filter_by(password=pw).first()
    user_id = user.user_id
    plants = {}
    if user:
        plants = user_plant.query.filter_by(user_id=user_id).all()
        print(plants)
    return render_template("myPlants.html", plants=plants)

@app.route('/deletePlant', methods=['GET', 'POST'])
def deletePlant():
    id = request.data
    plant = json.loads(id, object_hook=lambda d: SimpleNamespace(**d))
    print(plant.id)
    # plant = user_plant.query.filter(plant_id = id).delete()


@app.route('/keep_alive')
def keep_alive():
    global alive, data
    alive += 1
    keep_alive_count = str(alive)
    data['keep_alive'] = keep_alive_count
    parsed_json = json.dumps(data)
    return str(parsed_json)



if __name__ == "__main__":
    app.run(debug=True)
