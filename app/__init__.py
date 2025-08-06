from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_babel import Babel
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()
moment = Moment()
babel = Babel()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    babel.init_app(app)

    # Set up login configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.doctor import bp as doctor_bp
    app.register_blueprint(doctor_bp, url_prefix='/doctor')

    from app.pharmacy import bp as pharmacy_bp
    app.register_blueprint(pharmacy_bp, url_prefix='/pharmacy')

    from app.laboratory import bp as lab_bp
    app.register_blueprint(lab_bp, url_prefix='/laboratory')

    # Create upload directory if it doesn't exist
    import os
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Register error handlers
    from app.errors import init_error_handlers
    init_error_handlers(app)

    return app

from app import models