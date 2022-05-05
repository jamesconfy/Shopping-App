from flask import Flask
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'loginProducer' or 'loginConsumer'
login_manager.login_message_category = 'info'


def create_app():
    app = Flask('shoppingapp')
    app.config.from_object(DevConfig)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from shoppingapp import routes
        db.create_all()

    return app