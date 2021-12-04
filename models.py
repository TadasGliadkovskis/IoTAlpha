from greenhouse import db

#Model for the MYSQLAlchemy library
class users(db.Model):
    user_id = db.Column(db.String, primary_key=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    #Print user
    def __repr__(self):
        return f"User('{self.username}', '{self.name}')"


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
    user_id = db.Column(db.String, primary_key=True, nullable=False)
    plant_name = db.Column(db.String, primary_key=True, nullable=False)
    watered = db.Column(db.DateTime)
    planted = db.Column(db.Date, nullable=False)

    #Print user plant
    def __repr__(self):
        return f"User plant('{self.plant_id}', '{self.user_id}', '{self.plant_name}', '{self.watered}', '{self.planted}')"


class plant_readings(db.Model):
    plant_id = db.Column(db.String, nullable=False)
    raspi_id = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, nullable=False)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    soil_moisture = db.Column(db.String)

    # Print plant readings
    def __repr__(self):
        return f"Plant readings('{self.plant_id}', '{self.temperature}', '{self.humidity}', '{self.soil_moisture}')"

# How it works ? explained here
# https://www.youtube.com/watch?v=cYWiDiIUxQc&t=186s

# Need to create plant and other models
