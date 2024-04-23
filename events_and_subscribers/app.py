from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.events import NewRequest, NewResponse, subscriber

@view_config(
    route_name = 'home'
)

def home(request):
    return Response('Welcome!')

@subscriber(NewRequest,NewResponse)
def mysubscriber(event):
    print(event)

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('home','/')
        config.scan()
        app = config.make_wsgi_app()
        
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()