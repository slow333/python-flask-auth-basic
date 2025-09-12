import os

from flask import Flask, render_template
from . import auth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # The DATABASE key is now a PostgreSQL connection string.
        # It's configured to use the DATABASE_URL environment variable.
        # A default value is provided for development.
        DATABASE=os.environ.get('DATABASE_URL', 'postgresql://postgres:1111@localhost/flaskr'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    from . import db
    db.init_app(app)

    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    from . import todo
    app.register_blueprint(todo.bp)

    @app.route('/home')
    def home():
        return render_template('home.html')

    return app