from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config

from pyramid.session import SignedCookieSessionFactory
my_session_factory = SignedCookieSessionFactory('itsaseekreet')

from pyramid.csrf import get_csrf_token, new_csrf_token

@view_config(route_name = 'home', renderer = 'json')
def home(request):
    return {'msg':'CSRF Tokens in Pyramid'}

@view_config(route_name = 'get_token', renderer = 'json', require_csrf = True)
def get_token(request):
    token = get_csrf_token(request)
    print(token)
    return {'msg':'Get CSRF token'}

@view_config(route_name = 'new_token', renderer = 'json')
def new_token(request):
    token = new_csrf_token(request)
    print(token)
    return {'msg':'New CSRF token'}
    
    
# @view_config(route_name = 'myview', renderer= 'templates/home.jinja2')
# def myview(request):
#     return {'msg':'CSRF token in template'}

if __name__ == '__main__':
    with Configurator() as config:
        config.include('pyramid_jinja2')
        config.add_route('home','/')
        config.add_route('get_token','/token')
        config.add_route('new_token','/new_token')
        # config.add_route('myview','/myview')
        config.scan()
        config.set_session_factory(my_session_factory)
        config.set_default_csrf_options(require_csrf=True)
        app = config.make_wsgi_app()
        
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
    
    