import os
from flask import Flask
from flask_bcrypt import Bcrypt
from stck.database import db_session

# application factory
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'stck.sqlite')
    )

    bcrypt = Bcrypt(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # hello faf
    @app.route('/hello')
    def hello():
        return 'Hey faf'

    # killed app behaviour
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app
