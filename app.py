from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from tables import Users, Order, Offer
from datetime import date

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/my_db.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@app.route("/users", methods=["GET", "POST"])
def page_get_all_users():

    users = db.session.query(Users).all()

    all_users = []
    for user in users:
        new_user = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "age": user.age,
            "email": user.email,
            "role": user.role,
            "phone": user.phone
        }
        all_users.append(new_user)

    return jsonify(all_users)
    

@app.route("/users/<int:uid>", methods=["GET", "PUT", "DELETE"])
def page_get_user(uid):

    if request.method == "GET":
        user = db.session.query(Users).filter(Users.id == uid).all()[0]

        if user:

            user = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "age": user.age,
                "email": user.email,
                "role": user.role,
                "phone": user.phone
            }
            return jsonify(user)
        else:
            return "No such user", 404

    elif request.method == "PUT":
        user = request.get_json()[0]
        new_user = Users(
                          id=user["id"],
                          first_name=user["first_name"],
                          last_name=user["last_name"],
                          age=user["age"],
                          email=user["email"],
                          role=user["role"],
                          phone=user["phone"]
                          )
        with db.session.begin():
            db.session.add(new_user)
            db.session.commit()
        return "User added"

    elif request.method == "DELETE":
        user = db.session.query(Users).get(uid)
        db.session.delete(user)
        db.session.commit()
        return "User deleted"
    
    
@app.route("/orders")
def page_get_all_orders():
    orders = db.session.query(Order).all()

    all_orders = []

    for order in orders:
        new_order = {
            "id": order.id,
            "name": order.name,
            "description": order.description,
            "start_date": order.start_date,
            "end_date": order.end_date,
            "address": order.address,
            "price": order.price,
            "customer_id": order.customer_id,
            "executor_id": order.executor_id
        }
        all_orders.append(new_order)
    
    return jsonify(all_orders)
    

@app.route("/orders/<int:oid>", methods=["GET", "PUT", "DELETE"])
def page_get_order(oid):

    if request.method == "GET":
        order = db.session.query(Order).filter(Order.id == oid).all()[0]
        if order:

            order = {
                "id": order.id,
                "name": order.name,
                "description": order.description,
                "start_date": order.start_date,
                "end_date": order.end_date,
                "address": order.address,
                "price": order.price,
                "customer_id": order.customer_id,
                "executor_id": order.executor_id
            }

            return jsonify(order)
        else:
            return "Order not found", 404

    elif request.method == "PUT":
        order = request.get_json()[0]
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

        with db.session.begin():
            db.session.add(new_order)
            db.session.commit()
        return "New order is added"

    elif request.method == "DELETE":
        order = db.session.query(Order).get(oid)
        db.session.delete(order)
        db.session.commit()
        return "Order deleted"
    

@app.route("/offers")
def page_get_all_offers():
    offers = db.session.query(Offer).all()

    all_offers = []

    for offer in offers:
        new_offer = {
            "id": offer.id,
            "order_id": offer.order_id,
            "executor_id": offer.executor_id
        }
        all_offers.append(new_offer)

    return jsonify(all_offers)
    

@app.route("/offers/<int:oid>", methods=["GET", "PUT", "DELETE"])
def page_get_offer(oid):

    if request.method == "GET":

        offer = db.session.query(Offer).filter(Offer.id == oid).all()[0]

        if offer:
            offer = {
                "id": offer.id,
                "order_id": offer.order_id,
                "executor_id": offer.executor_id
            }
            return jsonify(offer)
        else:
            return "Offer not found", 404

    elif request.method == "PUT":
        offer = request.get_json()[0]
        new_offer = Offer(
            id=offer["id"],
            order_id=offer["order_id"],
            executor_id=offer["executor_id"]
        )

        with db.session.begin():
            db.session.add(new_offer)
            db.session.commit()
        return "New offer is added"

    elif request.method == "DELETE":
        offer = db.session.query(Offer).get(oid)
        db.session.delete(offer)
        db.session.commit()
        return "Offer deleted"


if __name__ == "__main__":
    app.run(port=8000, debug=True)
