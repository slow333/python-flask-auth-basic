from flask import (
    Blueprint, abort, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
  db = get_db()
  with db.cursor() as cursor:
    blogs = cursor.execute(
      'SELECT b.id, title, body, created, author_id, username'
      ' FROM blog b JOIN users u ON b.author_id = u.id'
      ' ORDER BY created DESC'
    )
    # db.commit()
    blogs = cursor.fetchall()

  return render_template('blog/index.html', blogs=blogs)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create_blog_post():
  if request.method == 'POST':
    title = request.form['title']
    body = request.form['body']
    error = None

    if not title:
      error = 'Title is required.'

    if error is not None:
      flash(error)
    else:
      db = get_db()
      db.cursor().execute(
          'INSERT INTO blog (title, body, author_id) VALUES (%s, %s, %s)',
          (title, body, g.user['id'])
        )
      db.commit()
      return redirect(url_for('blog.index'))

  return render_template('blog/create.html')

def get_blog(id, check_author=True):
  db = get_db()
  with db.cursor() as cursor:
    blog = cursor.execute(
      'SELECT b.id, title, body, created, author_id, username'
      ' FROM blog b JOIN users u ON b.author_id = u.id'
      ' WHERE b.id = %s',
      (id,)
    )
    blog = cursor.fetchone()

  if blog is None:
      abort(404, f"Blog id {id} doesn't exist.")

  if check_author and blog['author_id'] != g.user['id']:
      abort(403) #Forbidden

  return blog

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
  blog = get_blog(id)

  if request.method == 'POST':
    title = request.form['title']
    body = request.form['body']
    error = None

    if not title:
      error = 'Title is required.'

    if error is not None:
      flash(error)
    else:
      db = get_db()
      db.cursor().execute(
          'UPDATE blog SET title = %s, body = %s'
          ' WHERE id = %s',
          (title, body, id)
        )
      db.commit()
      
      return redirect("/")

  return render_template('blog/update.html', blog=blog)

@bp.route('/<int:id>/delete', methods=('POST', 'GET'))
@login_required
def delete(id):
  if request.method == 'POST':
    get_blog(id)
    db = get_db()
    db.cursor().execute(
      'DELETE FROM blog WHERE id = %s',
      (id,)
    )
    db.commit()
    return redirect(url_for('blog.index'))
  else:
    blog = get_blog(id)
    return render_template('blog/delete.html', blog=blog)