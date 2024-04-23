from pyramid.view import view_config
from main import session
from .models import User, Book, Role, user_roles
from middleware import MyMiddleware
from pyramid.view import forbidden_view_config
from .schemas import UserSchema
from pyramid.response import Response
import json
from marshmallow import ValidationError

@forbidden_view_config(renderer='json')
def forbidden(message,request):
    body = {
        "message": str(message),
        "status": 403
    }
    request.response.status = 403
    return body

def authenticate_user(username, password):
    login_query = session.query(User).\
        filter(User.username == username).\
        filter(User.password == password).first()

    if login_query:
        user_dict = {
            'userid': login_query.id,
            'user_name': login_query.username
        }
        
        return user_dict
    else:
        return None

@view_config(route_name='home', renderer='json')
def home(request):
    return {'msg':'Welcome to the Pyramid Framework!'}

@view_config(route_name = 'register',request_method= 'POST', renderer= 'json')
def register_users(request):
    
    schema = UserSchema()
    try:
        user_data, errors = schema.load(request.json_body)
    except ValidationError as e:
        return {'errors': e.messages}
    
    username = user_data.get('username')
    password = user_data.get('password')
    
    existing_user = session.query(User).filter_by(username=username).first()
    existing_password = session.query(User).filter_by(password=password).first()
    
    if existing_user:
        return {"message": "Username already exists. Choose a different username"}
        
    if existing_password:
        return {"message": "Password already exists. Create a new password"}
        
    new_user = User(username = username, password = password)
    session.add(new_user)
    session.commit()
    
    return {
        'msg':'User created successfully!'
        }
    
@view_config(route_name = 'login',request_method= 'POST', renderer= 'json')
def login(request):
    username = request.json_body.get('username')
    password = request.json_body.get('password')
        
    user = authenticate_user(username, password)
    if user:
        user_id = user['userid']
        jwt_token = request.create_jwt_token(user_id,name = username)
        return {
            'result': 'Login Successful!',
            'token': jwt_token
        }
        
    else:
        return {
            'result': 'Invalid credentials',
            'token': None
        }
        
@view_config(route_name = 'view_users', request_method = 'GET', renderer = 'json')
def view_users(request):
    data = session.query(User).all()
    
    data = [{'id': info.id,'username': info.username, 'password': info.password} for info in data]
    return {'data':data}

@view_config(route_name = 'view_users_by_id', request_method= 'GET', renderer= 'json')
def view_users_by_id(request):
    try:
        data = session.query(User).get(int(request.matchdict['id'])).to_json()
    
    except:
        return {'msg':'No data available'}
    
    return {'data':data}

@view_config(route_name = 'update_users', request_method= 'PUT', renderer= 'json')
def update_users(request):
    try:
        user_id = request.matchdict['id']
        user = session.query(User).filter(User.id == user_id).one()
        
        if 'username' in request.json_body:
            user.username = request.json_body['username']
        if 'password' in request.json_body:
            user.password = request.json_body['password']
            
        session.commit()
        
        return {'msg': 'Data updated successfully!'}
    
    except:
        return {'msg':'No data available'}
    
@view_config(route_name = 'delete_users', request_method= 'DELETE', renderer= 'json')
def delete_users(request):
    try:
        user_id = request.matchdict['id']
        user = session.query(User).filter(User.id == user_id).one()
        
        session.delete(user)
        session.commit()
        
        return {'msg': 'User deleted successfully!'}
    
    except:
        return {'msg':'No data available'}
    
@view_config(route_name= 'view_books', request_method = 'GET', renderer = 'json',permission='view')
def view_books(request):
    data = session.query(Book).all()
    
    books_data = [{'id': book.id,'title': book.title, 'author': book.author} for book in data]
    
    return {'data':books_data}

@view_config(route_name = 'view_books_by_id', request_method= 'GET', renderer= 'json')
def view_books_by_id(request):
    try:
        data = session.query(Book).get(int(request.matchdict['id'])).to_json()
    
    except:
        return {'msg':'No data available'}
    
    return {'data':data}

@view_config(route_name = 'add_books',request_method= 'POST', renderer= 'json', permission= 'create', decorator = MyMiddleware)
def create_books(request):
    if request.authenticated_userid:
        title = request.json_body.get('title')
        author = request.json_body.get('author')
        
        new_book = Book(title=title, author=author)
        session.add(new_book)
        session.commit()
        
        return {
            'msg': 'Book created successfully!',
            'data': {
                'id': new_book.id,
                'title': new_book.title,
                'author': new_book.author
        }
    }
        
@view_config(route_name = 'update_books', request_method= 'PUT', renderer= 'json')
def update_books(request):
    try:
        book_id = request.matchdict['id']
        book = session.query(Book).filter(Book.id == book_id).one()
        
        if 'title' in request.json_body:
            book.title = request.json_body['title']
        if 'author' in request.json_body:
            book.author = request.json_body['author']
            
        session.commit()
        
        return {'msg': 'Data updated successfully!'}
    
    except:
        return {'msg':'No data available'}
    
@view_config(route_name = 'delete_books', request_method= 'DELETE', renderer= 'json')
def delete_books(request):
    try:
        book_id = request.matchdict['id']
        book = session.query(Book).filter(Book.id == book_id).one()
        
        session.delete(book)
        session.commit()
        
        return {'msg': 'Book deleted successfully!'}
    
    except:
        return {'msg':'No data available'}
    
@view_config(route_name = 'create_roles',request_method= 'POST',renderer= 'json',permission = 'create')
def create_roles(request):
        name = request.json_body.get('name')
        
        new_role = Role(name = name)
        session.add(new_role)
        session.commit()
        
        return {
            'msg':'Role created successfully!',
            'data':{
                'id':new_role.id,
                'name':new_role.name
            }
        }
    
@view_config(route_name= 'view_roles', request_method = 'GET', renderer = 'json')
def view_roles(request):
    data = session.query(Role).all()
    
    data = [{'id': info.id,'role_name': info.name} for info in data]
    
    return {'data':data}
    
@view_config(route_name = 'create_users_roles',request_method= 'POST', renderer= 'json')
def create_users_roles(request):
    user_id = request.json_body.get('user_id')
    role_id = request.json_body.get('role_id')
    
    user = session.query(User).filter_by(id = user_id).first()
    role = session.query(Role).filter_by(id = role_id).first()
    
    if user and role:
        # Assign the role to the user
        user.roles.append(role)
        session.commit()
        return {
            'msg': f"User's role created successfully!",
            'data': {
                'user_id': user_id,
                'role_id': role_id
            }
        }
    else:
        return {
            'error': 'User or role does not exist!'
        }
        
@view_config(route_name= 'view_users_roles', request_method = 'GET', renderer = 'json')
def view_users_roles(request):
    data = session.query(user_roles).all()
    
    data = [{'user_id': info.user_id,'role.id': info.role_id} for info in data]
    
    return {'data':data}

