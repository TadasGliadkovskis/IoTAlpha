from flask import Flask
import uuid
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import logging
secret = uuid.uuid4()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:@localhost/greenhouse'
app.config["SECRET_KEY"] = f"{secret}"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
logger = logging.getLogger(__name__)
from greenhouse import routes
