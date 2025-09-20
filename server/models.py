from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    restaurant_pizzas = db.relationship(
        'RestaurantPizza',
        back_populates='restaurant',
        cascade='all, delete'
    )

    def to_dict(self, include_pizzas=False):
        data = {
            "id": self.id,
            "name": self.name,
            "address": self.address
        }
        if include_pizzas:
            data["restaurant_pizzas"] = [rp.to_dict() for rp in self.restaurant_pizzas]
        return data


class Pizza(db.Model):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)

    restaurant_pizzas = db.relationship(
        'RestaurantPizza',
        back_populates='pizza',
        cascade='all, delete'
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "ingredients": self.ingredients
        }


class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)

    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')
    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')

    def __init__(self, price, pizza_id, restaurant_id):
        if not self.validate_price(price):
            raise ValueError("Price must be between 1 and 30")
        self.price = price
        self.pizza_id = pizza_id
        self.restaurant_id = restaurant_id

    @staticmethod
    def validate_price(price):
        return 1 <= price <= 30

    def to_dict(self):
        return {
            "id": self.id,
            "price": self.price,
            "pizza_id": self.pizza_id,
            "restaurant_id": self.restaurant_id,
            "pizza": self.pizza.to_dict(),
            "restaurant": {
                "id": self.restaurant.id,
                "name": self.restaurant.name,
                "address": self.restaurant.address
            }
        }
