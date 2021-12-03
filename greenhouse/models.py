from greenhouse import db, login_manager
from flask_login import UserMixin
from greenhouse import bcrypt
# Model for the MYSQLAlchemy library

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

class users(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    #Print user
    def __repr__(self):
        return f"User('{self.username}', '{self.name}')"

    def get_id(self):
        return (self.user_id)

    def hash(password):
        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        print(hashed)
        return hashed


class plants(db.Model):
    plant_name = db.Column(db.String, primary_key=True, nullable=False)
    ideal_lower_temperature = db.Column(db.Float, nullable=False)
    ideal_higher_temperature = db.Column(db.Float, nullable=False)
    ideal_soil_moisture = db.Column(db.Float, nullable=False)

    #Print plant
    def __repr__(self):
        return f"Plant('{self.plant_name}', '{self.ideal_lower_temperature}', '{self.ideal_higher_temperature}', '{self.ideal_soil_moisture}')"


class user_plant(db.Model):
    plant_id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, primary_key=True, nullable=False, foreign_key=True)
    plant_name = db.Column(db.String, primary_key=True, nullable=False, foreign_key=True)
    watered = db.Column(db.DateTime)
    planted = db.Column(db.Date, nullable=False)

    #Print user plant
    def __repr__(self):
        return f"User plant('{self.plant_id}', '{self.user_id}', '{self.plant_name}', '{self.watered}', '{self.planted}')"

class plant_readings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.String, nullable=False, foreign_key=True)
    raspi_id = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, nullable=False, foreign_key=True)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    soil_moisture = db.Column(db.String)

    # Print plant readings
    def __repr__(self):
        return f"Plant readings('{self.plant_id}',{self.raspi_id},{self.user_id}, '{self.temperature}', '{self.humidity}', '{self.soil_moisture}')"
