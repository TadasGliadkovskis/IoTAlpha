from flask import render_template, redirect, url_for, request, flash, make_response
from greenhouse.forms import RegistrationForm, LoginForm, plantForm
import uuid
from greenhouse import db, bcrypt, app, logger
from greenhouse.models import users as User, plant_readings
from flask_login import login_user, current_user
import json
from types import SimpleNamespace
# import apperror as AppError
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


alive = 0
data = {}


@app.route('/register', methods=['GET', 'POST'])
def register():
    # generate ID for user
    users_id = uuid.uuid4().int
    form = RegistrationForm(request.form)

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
        print(new_user.password)
        # Create an instance of the User class

        db.session.add(new_user)  # Adds new User record to database
        db.session.commit()  # Commits all changes
        return redirect(url_for('loginPage2'))
    return render_template('loginPage2.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit:
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("myPlants"))
        else:
            flash('login unsuccessful check username and password')
    return render_template('loginPage2.html', form=form)


@app.route("/", methods=['GET', 'POST'])
def loginPage2():
    form = RegistrationForm(request.form)
    return render_template("loginPage2.html", form=form)


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


@app.route("/custom")
def custom():
    return render_template("custom.html")


@app.route("/index")
def index():
    return render_template("index.html")


@app.route('/myPlants')
def myPlants():
    return render_template("myPlants.html")


@app.route('/keep_alive')
def keep_alive():
    global alive, data
    alive += 1
    keep_alive_count = str(alive)
    data['keep_alive'] = keep_alive_count
    parsed_json = json.dumps(data)
    return str(parsed_json)


@app.route("/status=<name>-<action>", methods=["POST"])
def event(name, action):
    global data
    print("Got " + name + ", action: " + action)
    if name == "buzzer":
        if action == "ON":
            data["alarm"] = True
        elif action == "OFF":
            data["alarm"] = False
    return str("OK")


if __name__ == "__main__":
    app.run(debug=True)
