import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def setup_db(app):
    database_name = 'joshuas' # Local psql test
    # password = 'mongoose1'
    password = 'mongoose1'
    default_database_path= "postgres://{}:{}@{}/{}".format('postgres', password, 'localhost:5432', database_name)
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


class User(db.Model):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(80), unique=True)
    email_address = Column(String(50))
    cellphone_number = Column(String(80), unique=True)

    def __init__(self, full_name, email_address, cellphone_number):
        self.full_name = full_name
        self.email_address = email_address
        self.cellphone_number = cellphone_number

    def details(self):
        return {
                'id': self.id,
                'full_name': self.full_name,
                'email_address': self.email_address,
                'cellphone_number': self.cellphone_number
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def as_dict(self):
       #return {c.name: getattr(self, c.name) for c in self.__table__.columns}
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class Order(db.Model):
    __tablename__ = 'food_orders'
    id = Column(Integer, primary_key=True)
    customer = Column(String(80), unique=True)
    food_item = Column(String(80))

    def __init__(self, customer, food_item):
        self.customer = customer
        self.food_item = food_item

    def details(self):
        return {
                'id': self.id,
                'customer': self.customer,
                'food_item': self.food_item
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def group_orders(self):
        result = db.session.execute('SELECT food_item, COUNT(food_item) FROM food_orders GROUP BY food_item')
        return result


class Food(db.Model):
    __tablename__ = 'foods'
    id = Column(Integer, primary_key=True)
    title = Column(String(80), unique=True)
    created_date = Column(db.DateTime)

    def __init__(self, title, created_date):
        self.title = title
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
