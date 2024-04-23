from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

# Define a simple view
def hello_world(request):
    return Response('Hello, World!')

# Define a middleware
class MyMiddleware:
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        # Do something before handling the request
        print("Middleware is handling the request")
        # Pass the request through to the next middleware or the Pyramid app
        response = self.app(environ, start_response)
        # Do something after handling the request
        print("Middleware is handling the response")
        return response
    
if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        # Create the Pyramid app
        app = config.make_wsgi_app()
    
    # Wrap the Pyramid app with the middleware
    app = MyMiddleware(app)

    # Create a WSGI server and run the app
    server = make_server('localhost', 8080, app)
    print("Server running on http://localhost:8080")
    server.serve_forever()
