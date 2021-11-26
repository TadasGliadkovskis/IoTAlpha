from flask import render_template, redirect, url_for, request, flash, make_response
from greenhouse.forms import RegistrationForm, LoginForm, plantForm
import uuid
from greenhouse import db, bcrypt
from greenhouse import app
from greenhouse.models import users as User, plant_readings
from flask_login import login_user, current_user
import json


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
            name=form.name.data,)
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


# @app.route('/plants', methods=["GET",'POST'])
# def defaultPlants():
#     defPlant = plants.query.all()
#     return render_template('plants.html', defPlant = defPlant)

@app.route("/", methods=['GET', 'POST'])
def loginPage2():
    form = RegistrationForm(request.form)
    return render_template("loginPage2.html", form=form)


@app.route("/sendPlants", methods=['GET', "POST"])
def sendPlants():


    form = request.form
    plant = plant_readings.query.filter_by(username=request.form.plant_id).first()
    user_id = plant.user_id
    if request.method == 'POST' and form.validate_on_submit():
        readings = plant_readings(

            user_id = user_id,
            plant_id=form.plant_id,
            temperature=form.temperature,
            humidity=form.humidity,
            soil_moisture=form.soil_moisture,
        )
        db.session.add(readings)
        db.session.commit()

    return render_template("myPlants.html", form=form)

@app.route("/custom")


def custom():
    return render_template("custom.html")


@app.route("/myPlants", methods=['GET', 'POST'])
def updatePlants():
    form = plantForm(request.form)
    return render_template("myPlants.html", form=form)


@app.route('/keep_alive')
def keep_alive():
    global alive, data
    alive += 1
    keep_alive_count = str(alive)
    data['keep_alive'] = keep_alive_count
    parsed_json = json.dumps(data)
    return str(parsed_json)


@app.route('/stats', methods=["POST", "GET"])
def stats():
    data = request.decode("utf-8")
    print(data.temperature)
    return render_template("myPlants.html", data=data)




@app.route("/status=<name>-<action>", methods=["POST"])
def event(name, action):
    global data
    print("Got " + name + ", action: " + action)

@app.route("/myPlants")
def myPlants():
    return render_template("myPlants.html")

@app.route("/index.html")
def index():
    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True)
