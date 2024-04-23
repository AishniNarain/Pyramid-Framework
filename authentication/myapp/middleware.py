from pyramid.request import Request
from pyramid.response import Response

class MyMiddleware:
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        # Do something before handling the request
        print("Middleware is handling the request")
        # Pass the request through to the next middleware or the Pyramid app
        response = self.app(environ, start_response)
        # print(response)
        # # # Do something after handling the request   
        # # print("Middleware is handling the response")
        return response
    
