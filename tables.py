from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import date


def load_from_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        result = json.load(file)
    return result


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/my_db.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(20))


class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    users = db.relationship("Users", foreign_keys=[executor_id])
    order = db.relationship("Order", foreign_keys=[order_id])


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String(1000))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    users1 = db.relationship("Users", foreign_keys=[customer_id])
    users2 = db.relationship("Users", foreign_keys=[executor_id])
    

db.drop_all()
db.create_all()


print("------------------------------LOADING ORDERS------------------------------")
orders = load_from_json("orders.json")
all_orders = []
for order in orders:
    dates = [int(i) for i in order["start_date"].split("/")]
    order["start_date"] = date(dates[2], dates[0], dates[1])
    dates = [int(i) for i in order["end_date"].split("/")]
    order["end_date"] = date(dates[2], dates[0], dates[1])
    new_order = Order(
        id=order["id"],
        name=order["name"],
        description=order["description"],
        start_date=order["start_date"],
        end_date=order["end_date"],
        address=order["address"],
        price=order["price"],
        customer_id=order["customer_id"],
        executor_id=order["executor_id"]
    )
    all_orders.append(new_order)
print("------------------------------ORDERS LOADED------------------------------")


print("------------------------------LOADING OFFERS------------------------------")
offers = load_from_json("offers.json")
all_offers = []
for offer in offers:
    new_offer = Offer(
        id=offer["id"],
        order_id=offer["order_id"],
        executor_id=offer["executor_id"]
    )
    all_offers.append(new_offer)
print("------------------------------OFFERS LOADED------------------------------")


print("------------------------------LOADING USERS------------------------------")
users = load_from_json("users.json")
all_users = []
for user in users:
    new_user = Users(
        id=user["id"],
        first_name=user["first_name"],
        last_name=user["last_name"],
        age=user["age"],
        email=user["email"],
        role=user["role"],
        phone=user["phone"]
    )
    all_users.append(new_user)
print("------------------------------USERS LOADED------------------------------")


print("______________________________STARTING SESSION______________________________")
with db.session.begin():
    try:
        print("trying to add users... ", end="")
        db.session.add_all(all_users)
        print("done")
    except Exception.SQLAlchemy as err:
        print(err)
    finally:
        try:
            print("trying to add orders... ", end="")
            db.session.add_all(all_orders)
            print("done")
        except Exception.SQLAlchemy as err:
            print(err)
        finally:
            try:
                print("trying to add offers... ", end="")
                db.session.add_all(all_offers)
                print("done")
            except Exception.SQLAlchemy as err:
                print(err)
