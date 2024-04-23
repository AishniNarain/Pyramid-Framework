import sys
import os


# Add the parent directory of 'myapp' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from wsgiref.simple_server import make_server
from myapp import main

from models import getsession
session=getsession()

if __name__ == '__main__':
    
    app = main({})
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
