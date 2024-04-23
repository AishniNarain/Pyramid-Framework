from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .security import RootACL
from middleware import MyMiddleware

def main(global_config, **settings):
    config = Configurator(settings=settings, root_factory=RootACL)
    
    # Set up authorization policies
    config.set_authorization_policy(ACLAuthorizationPolicy())

    # Enable JWT authentication.
    config.include('pyramid_jwt')
    config.set_jwt_authentication_policy('secret', auth_type='Bearer')
    # config.set_root_factory(RootACL)
    
    # config.include(authorization_middleware)
    
    # Including routes
    config.include('myapp.routes')
    config.scan()
    
    app = config.make_wsgi_app()  # Create the WSGI application
    
    # Wrap the WSGI application with MyMiddleware
    # app = MyMiddleware(app)
    
    return app
