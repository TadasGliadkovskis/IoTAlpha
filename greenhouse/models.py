from greenhouse import db

#Model for the MYSQLAlchemy library
class users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    #Print user
    def __repr__(self):
        return f"User('{self.username}', '{self.name}', '{self.location}')"

# How it works ? explained here
# https://www.youtube.com/watch?v=cYWiDiIUxQc&t=186s

# Need to create plant and other models

