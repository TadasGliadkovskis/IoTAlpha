from flask import Flask
import uuid
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import logging


secret = uuid.uuid4()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin123@database-1.cmi49prbg0zg.us-east-2.rds.amazonaws.com/greenhouse'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SECRET_KEY"] = f"{secret}"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
logger = logging.getLogger(__name__)
from greenhouse import routes

if __name__ == '__main__':
    app.debug = True
    app.run()

