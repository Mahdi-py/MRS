from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Flask_MRS.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # The function name of the login route
login_manager.login_message_category = 'info'  # the class the flush massage of the user access unauthrized route
migrate= Migrate(app,db)
manager= Manager(app)

manager.add_command('db', MigrateCommand)

from Flask_MRS import routes