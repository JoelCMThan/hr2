from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app.blueprints.auth.routes import auth
    from app.blueprints.employee.routes import employee
    from app.blueprints.manager.routes import manager
    from app.blueprints.admin.routes import admin
    from app.errors.handlers import errors

    app.register_blueprint(auth)
    app.register_blueprint(employee)
    app.register_blueprint(manager)
    app.register_blueprint(admin)
    app.register_blueprint(errors)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User  # Import the User model here to avoid circular import
        return User.query.get(int(user_id))

    return app
