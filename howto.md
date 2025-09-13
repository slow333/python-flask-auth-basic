### python version에 따라 pip에서 설치되는 flask version, sqlalchemy, psycopg2 버전이 다름

### python 13 버젼 기준
```
Package           Version
----------------- -------
blinker           1.9.0
click             8.2.1
colorama          0.4.6
Flask             3.1.2
greenlet          3.2.4
itsdangerous      2.2.0
Jinja2            3.1.6
MarkupSafe        3.0.2
pip               25.2
psycopg2-binary   2.9.10
SQLAlchemy        2.0.43
typing_extensions 4.15.0
Werkzeug          3.1.3
```
이 버전에서 flask --app flaskr run --debug 가능함<br>
__init__.py 설정도 상위 python version에서 가능함
```
flaskr/__init__.py
import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
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

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
```
### run app : flask --app flaskr run --debug

### database 연결 설정(psycopg2)
```
flaskr/db.py
from flask import current_app, g

DATABASE = 'postgresql://postgres:1111@localhost/flaskr'

def get_db():
  if 'db' not in g:
    g.db = psycopg2.connect(DATABASE, cursor_factory=psycopg2.extras.DictCursor)
  return g.db

def close_db(e=None):
  """Close the database connection."""
  db = g.pop('db', None)

  if db is not None:
    db.close()

def init_db():
  db = get_db()

  with current_app.open_resource('schema.sql') as f:
    # psycopg2 requires a cursor to execute commands
    with db.cursor() as cur:
      cur.execute(f.read().decode('utf8'))
  # Commit the changes to make them persistent
  db.commit()

@click.command('init-db')
def init_db_command():
  """Clear the existing data and create new tables."""
  init_db()
  click.echo('Initialized the PostgreSQL database.')

def init_app(app):
  """Register database functions with the Flask app."""
  app.teardown_appcontext(close_db)
  app.cli.add_command(init_db_command)
```
### __init__.py 설정
```
    from . import db
    db.init_app(app)
```
### g is a special object that is unique for each request. It is used to store data that might be accessed by multiple functions during the request. The connection is stored and reused instead of creating a new connection if get_db is called a second time in the same request.

### run : flask --app flaskr init-db

### psycopg2에서 query 객체를 dict처럼 사용 가능하나 (user['id'])
> 여기서는 with conn.cursor() as cur: cur.execute('sql')
### sqlalchemy에서는 qeury 객체를 dict 처럼 안되고 tuple처럼 해야함(user[0])
> 여기서는 with engine.connect() as conn: conn.execute('sql')
## flask 버전에 따라 프로젝트에서 db sesstion 연결하는 방식이 다름

## 주의 할점
### 공통으로 select 처럼 return 값이 있으면 with 에서 fetch를 수행해야 하고,
> sqlalchemy
```
session_db = get_db()
session_db.execute(
    text('INSERT INTO blog (title, body, author_id) VALUES (:title, :body, :author_id)'),
    {'title': title, 'body': body, 'author_id': g.user['id']}
)
session_db.commit()

session_db = get_db()
result = session_db.execute(text(
  'SELECT b.id, title, body, created, author_id, username'
  ' FROM blog b JOIN users u ON b.author_id = u.id'
  ' ORDER BY created DESC'
))
blogs = result.fetchall()
```
> psycopg2
```
db = get_db()
db.cursor().execute(
  'UPDATE blog SET title = %s, body = %s  WHERE id = %s',
  (title, body, id)
)
db.commit()

session_db = get_db()
result = session_db.execute(text(
  'SELECT b.id, title, body, created, author_id, username'
  ' FROM blog b JOIN users u ON b.author_id = u.id'
  ' ORDER BY created DESC'
))
blogs = result.fetchall()
return render_template('blog/index.html', blogs=blogs)
```
# set env run script
```
$ cat ~/.bashrc
alias start="source /b/python/flask-tutorial/.venv/Scripts/activate"
alias run="flask --app flaskr run --debug"
```

# flask_crud 
### To run the app, 
### bash: export FLASK_APP=pybo, export FLASK_DEBUG=true , flask run
### cmd : set FLASK_APP=pybo, set FLASK_DEBUG=true, flask run