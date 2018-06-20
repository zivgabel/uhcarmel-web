
import click
from flask import current_app, g
from flask.cli import with_appcontext

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from passlib.apps import custom_app_context as pwd_context
import random, string


from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))



Base  = declarative_base();

def get_db():
    if 'db' not in g:
        engine = create_engine(current_app.config['DATABASE'])
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        g.db = DBSession()

    return g.db


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'mysql_charset':'utf8'}
    id = Column(Integer, primary_key = True)
    mirs = Column(String(10), nullable=False)
    password_hash = Column(String(100), nullable=False)
    first_name =Column(String(50), nullable = False)
    last_name =Column(String(50), nullable = False)
    google_sid = Column(String(100))
    google_email = Column(String(100))
    is_admin = Column(Boolean())
    address = Column(String(250))
    city = Column(String(100))
    def hash_password(self,password):
        self.password_hash = pwd_context.encrypt(password)
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=6000):
        s = Serializer(secret_key, expires_in = expiration)
        return s.dumps({'id': self.id })
    
    @staticmethod
    def verify_auth_token(token):
        print secret_key
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            print 'Valid Token, but expired'
            return None
        except BadSignature:
            print 'Invalid Token'
            return None
        user_id = data['id']
        return user_id

class PendingUser(Base):
    __tablename__ = 'pending_user'
    __table_args__ = {'mysql_charset':'utf8'}
    id = Column(Integer, primary_key = True)
    google_sid = Column(String(100))
    google_email = Column(String(100))



class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key = True)
    name =Column(String(250), nullable = False)
    altitude = Column(String(250), nullable = False)
    longitude = Column(String(250), nullable = False)
    
    @property
    def serialize(self):
        return {
           'id' : self.id,
           'name' : self.name,
           'altitude' : self.altitude,
           'longitude' : self.longitude
        }



def init_db():
    engine = create_engine(current_app.config['DATABASE'], isolation_level="AUTOCOMMIT")
    db = get_db()

    Base.metadata.create_all(engine)
    with current_app.open_resource('data.sql') as f:
        for line in f:
            db.execute(line.decode('utf8'))

        
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()