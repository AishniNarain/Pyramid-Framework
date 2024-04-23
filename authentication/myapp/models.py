from sqlalchemy.dialects.sqlite import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy import Table,Column, Integer, String,ForeignKey

from sqlalchemy.dialects.mysql import *

# SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"

MYSQL_DATABASE_URL = "mysql+pymysql://root:Abcdef123@localhost/pyramid"

Base = declarative_base()

#Association table for many-to-many relationship between User and Role tables
user_roles = Table('user_roles', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(50), unique=True)
    
    def __init__(self,id,username,password):
        self.id = id,
        self.username = username,
        self.password = password
        
    def to_json(self):
        to_serialize = ['id', 'username', 'password']
        d = {}
        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)
        return d
    
    roles = relationship("Role", secondary= user_roles, back_populates= "users")
    
class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    
    users = relationship("User", secondary= user_roles, back_populates= "roles")
    

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    author = Column(String(50))
    
    def __init__(self,id,title,author):
        self.id = id,
        self.title = title,
        self.author = author
        
    def to_json(self):
        to_serialize = ['id', 'title', 'author']
        d = {}
        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)
        return d
    
def getsession():
    # engine = create_engine(
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    engine = create_engine(MYSQL_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind = engine)
    session = Session()
    return session
    
    



