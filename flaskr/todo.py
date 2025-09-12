from flask import (
    Blueprint, abort, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
from datetime import datetime


bp = Blueprint('todo', __name__, url_prefix='/todo')

@bp.route('/')
def index():
  db = get_db()
  with db.cursor() as cursor:
    cursor.execute(
      'SELECT t.id, job, done, created, end_date, create_id, username'
      ' FROM todo t JOIN users u ON t.create_id = u.id'
      ' ORDER BY created DESC'
    )
    todos = cursor.fetchall()

  return render_template('todo/index.html', todos=todos)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create_todo_post():
  if request.method == 'POST':
    job = request.form['job']
    end_date = request.form['end_date']
    error = None

    if not job:
      error = 'job is required.'
    if end_date == '':
      end_date = datetime.now()

    if error is not None:
      flash(error)
    else:
      db = get_db()
      db.cursor().execute(
          'INSERT INTO todo (job, end_date, create_id) VALUES (%s, %s, %s)',
          (job, end_date, g.user['id'])
        )
      db.commit()
      return redirect(url_for('todo.index'))

  return render_template('todo/create.html')

def get_todo(id):
  db = get_db()
  with db.cursor() as cursor:
    todo = cursor.execute(
      'SELECT t.id, job, end_date, done, created, create_id, username'
      ' FROM todo t JOIN users u ON t.create_id = u.id'
      ' WHERE t.id = %s',
      (id,)
    )
    todo = cursor.fetchone()

  if todo is None:
      abort(404, f"todo id {id} doesn't exist.")

  if todo['create_id'] != g.user['id']:
      abort(403) #Forbidden

  return todo

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
  todo = get_todo(id)
  todo['end_date'] = todo['end_date'].date()

  if request.method == 'POST':
    job = request.form['job']
    end_date = request.form['end_date']
    done = request.form.get('done')
    error = None

    if not job:
      error = 'Title is required.'
    if end_date is None:
      end_date = todo['end_date']
    if done is None:
      done = False

    if error is not None:
      flash(error)
    else:
      db = get_db()
      db.cursor().execute(
          'UPDATE todo SET job = %s, end_date = %s, done = %s'
          ' WHERE id = %s',
          (job, end_date, done, id)
        )
      db.commit()
      
      return redirect("/todo/")

  return render_template('todo/update.html', todo=todo)

@bp.route('/<int:id>/delete', methods=('POST', 'GET'))
@login_required
def delete(id):
  todo = get_todo(id)
  if request.method == 'POST':
    db = get_db()
    db.cursor().execute(
      'DELETE FROM todo WHERE id = %s',
      (id,)
    )
    db.commit()
    return redirect('/todo/')
  else:
    todo = get_todo(id)
    return render_template('todo/delete.html', todo=todo)