import os
from flask import Flask

from flaskr.auth import bp as auth_bp  # Import the auth blueprint
from flaskr.blog import bp as blog_bp  # Import the blog blueprint

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
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

    # Register the blueprints with the correct aliases
    app.register_blueprint(auth_bp)  # Register auth blueprint
    app.register_blueprint(blog_bp)  # Register blog blueprint

    from . import db  # Import db here
    db.init_app(app)  # Register db functions

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app

