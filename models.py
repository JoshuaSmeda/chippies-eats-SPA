import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
'''
setup_db(app):
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app):
    database_name = 'joshua.s' # Local psql test
    default_database_path= "postgres://{}:{}@{}/{}".format('postgres', 'password', 'localhost:5432', database_name)
    database_path = os.getenv('DATABASE_URL', default_database_path) # Heroku
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

'''
Drops the database tables and starts fresh, can be used to initialize a clean database
'''

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

class Food(db.Model):
    __tablename__ = 'food'
    id = Column(Integer, primary_key=True)
    title = Column(String(80), unique=True)
    created_date = Column(db.DateTime)

    def __init__(self, title, created_date):
        self_title = title
        self.created_date = created_date

    def details(self):
        return {
                'id': self.id,
                'title': self.title,
                'created_date': self.created_date
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
