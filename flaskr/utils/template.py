def body_template(nav, content, id=None):
    contextUI = ''
    if id != None:
        contextUI = f'''
        <a href="/topic/{id}/edit">Edit</a>
        <a href="/topic/{id}/delete">Delete</a>
        '''
    return f'''
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <link rel="stylesheet" href="/static/style.css">
      <link rel="stylesheet" href="/static/flask.css">
      <title>flask CRUD</title>
    </head>
    <body>
        <ul class="topc_nav">
            <li><a href="/blog/">Blogs</a></li>
            <li><a href="/todo/">Todo</a></li>
            <li><a href="/topic/">Topics</a></li>
        </ul>
        <ol class="flask_nav">
            {nav}
        </ol>
        <div class="flask_content">
            {content}
        </div>
        <div class='flask_links'>
            <a href="/topic/create">Create</a>
            {contextUI}
        </div>
    </body>
    </html>
    '''
def getNav(topics):
    nav_items = [f'<li><a href="/topic/{item["id"]}">{item["title"]}</a></li>' for item in topics]
    return "\n".join(nav_items)

topics = [
    {"id": 1, "title": "Flask", "content": "Flask is a micro web framework for Python."},
    {"id": 2, "title": "Django", "content": "Django is a high-level Python web framework."},
    {"id": 3, "title": "FastAPI", "content": "FastAPI is a modern web framework for building APIs."}
]