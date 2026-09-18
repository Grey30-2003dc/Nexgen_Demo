import logging
from flask import Flask
from app.config import Config
from app.extensions import db


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    db.init_app(app)

    from app.api.auth import bp as auth_bp
    from app.api.employees import bp as employees_bp
    from app.api.departments import bp as departments_bp
    from app.api.reports import bp as reports_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(departments_bp)
    app.register_blueprint(reports_bp)

    with app.app_context():
        db.create_all()
    logging.basicConfig(level=logging.DEBUG)
    return app
