from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Flask_MRS.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from Flask_MRS import routes