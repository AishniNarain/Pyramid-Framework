from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from pyramid.view import view_config
from pyramid.csrf import check_csrf_token
from pyramid.httpexceptions import HTTPFound

my_session_factory = SignedCookieSessionFactory('mysecret')

@view_config(route_name='home', renderer='templates/home2.jinja2')
def home(request):
    csrf_token = request.session.get_csrf_token()
    print(csrf_token)
    return {'csrf_token': csrf_token}

@view_config(route_name='submit', request_method='POST')
def submit(request):
    # Ensure CSRF token is valid
    check_csrf_token(request)
    
    # Process form submission
    # (code to handle form submission goes here)

    # Redirect or render a response
    return HTTPFound(location='/success')

@view_config(route_name='success', renderer = 'json')
def success(request):
    return {'msg':'Form submitted successfully'}

if __name__ == '__main__':
    # Configure Pyramid application
    with Configurator() as config:
        config.set_session_factory(my_session_factory)
        config.include('pyramid_jinja2')
        config.add_route('home', '/')
        config.add_route('submit', '/submit')
        config.add_route('success', '/success')
        config.scan()
        app = config.make_wsgi_app()
        
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()