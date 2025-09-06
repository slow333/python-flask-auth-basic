from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.db import get_db

bp = Blueprint('blog', __name__, url_prefix='/blog')

@bp.route('/create', methods=('GET', 'POST'))
def create_post():
  if request.method == 'POST':
    title = request.form['title']
    content = request.form['content']
    db = get_db()
    error = None

    if not title:
      error = 'Title is required.'
    elif not content:
      error = 'Content is required.'
    else:
      try:
        with db.cursor() as cur:
          cur.execute(
            "INSERT INTO blog (title, content) VALUES (%s, %s)",
            (title, content)
          )
          cur.execute("SELECT * FROM blog ORDER BY created DESC")
          blogs = cur.fetchall()
        db.commit()
      except db.IntegrityError:
        error = f"Post with title {title} already exists."

    if error is None:
      return redirect(url_for('blog.index'), blogs=blogs)

    flash(error)

  return render_template('blog/create.html')