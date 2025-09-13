import psycopg2
import psycopg2.extras

import click
from flask import current_app, g

DATABASE = 'postgresql://postgres:1111@localhost/flaskr'

def get_db():
  """Get a database connection from the application context."""
  if 'db' not in g:
    g.db = psycopg2.connect(DATABASE, cursor_factory=psycopg2.extras.DictCursor)
  return g.db

def close_db(e=None):
  """Close the database connection."""
  db = g.pop('db', None)

  if db is not None:
    db.close()

def init_db():
  """Initialize the database with the schema."""
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