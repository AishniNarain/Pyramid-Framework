from wsgiref.simple_server import make_server
from pyramid.response import Response

# Custom middleware for authorization
def authorization_middleware(handler):
    def middleware(environ, start_response):
        print("Middleware executing before handling the request")
        # Call the actual handler
        response = handler(environ, start_response)
        print("Middleware executing after handling the request")
        return response
    return middleware

# Add a custom view
def hello_world(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b'Hello, World!']

if __name__ == '__main__':
    # Create a WSGI application
    app = hello_world
    
    # Wrap the WSGI application with the middleware
    app = authorization_middleware(app)
    
    # Serve the app using a simple WSGI server
    server = make_server('0.0.0.0', 6543, app)
    print("Serving on http://0.0.0.0:6543")
    server.serve_forever()
