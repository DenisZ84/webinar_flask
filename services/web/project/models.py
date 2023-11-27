from . import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email):
        self.email = email


class Price(db.Model):
    __tablename__ = 'fuel_prices'
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(255))
    price = db.Column(db.Float())
    date = db.Column(db.DateTime())