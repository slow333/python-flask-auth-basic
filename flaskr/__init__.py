import os

from .utils.template import body_template as body, getNav as nav, topics
from flask import Flask, render_template
from .bp import auth

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

    from .bp import blog
    app.register_blueprint(blog.bp)
    # app.add_url_rule('/', endpoint='index')

    from .bp import todo
    app.register_blueprint(todo.bp)

    from .bp import topic_nodb
    app.register_blueprint(topic_nodb.bp)

    # a simple page that says hello

    @app.route('/')
    def home():
        return render_template('home.html')
    
    @app.route("/install")
    def install():
        return body(nav(topics), render_template("install.html"))

    return app

# if __name__ == "__main__":
# app.run(debug=True, host='0.0.0.0', port=5000)
# To run the app, 
# bash: export FLASK_APP=pybo, export FLASK_DEBUG=true , flask run
# cmd : set FLASK_APP=pybo, set FLASK_DEBUG=true, flask run