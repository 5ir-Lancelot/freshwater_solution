# wsgi.py

from your_first_flask_app import app as first_app
from your_second_flask_app import app as second_app

def application(environ, start_response):
    path_info = environ['PATH_INFO']

    # If the path is '/', serve the main page
    if path_info == '/':
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'<h1>Welcome to the Main Page</h1>']

    # If the path starts with '/first', route to the first app
    elif path_info.startswith('/first'):
        return first_app(environ, start_response)

    # For all other paths, route to the second app
    else:
        return second_app(environ, start_response)