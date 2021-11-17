from flask import Flask
import uuid
from flask_sqlalchemy import SQLAlchemy

secret = uuid.uuid4()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:@localhost/greenhouse'
app.config["SECRET_KEY"] = f"{secret}"
db = SQLAlchemy(app)

from greenhouse import routes
