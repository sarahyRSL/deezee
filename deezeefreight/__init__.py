
import os
import random
from flask import Flask
from dotenv import load_dotenv
from .auth import bp as auth_bp
from .routes import bp as routes_bp

load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_mapping(
        SECRET_KEY=random.random(),
        SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids a warning
    )
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    app.register_blueprint(routes_bp)
    app.register_blueprint(auth_bp)

    return app
