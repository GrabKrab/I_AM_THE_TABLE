from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.DevConfig')
    app.config['FLASK_ENV'] = 'development'

    app.jinja_env.filters['zip'] = zip
    app.jinja_env.filters['enumerate'] = enumerate

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from .table.routes import table_bp
        # from .profile.routes import profile_bp
        from .profile.auth import auth_bp

        # Register Blueprints
        app.register_blueprint(table_bp)
        # app.register_blueprint(profile_bp)
        app.register_blueprint(auth_bp)

        db.create_all()

        return app
