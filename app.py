import os, uuid, simplejson
from flask import Flask, request, abort, jsonify, render_template
from flask_cors import CORS
from models import setup_db, Food, Order, User, db_drop_and_create_all
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

def create_app(test_config=None):
    app = Flask(__name__)
    app._static_folder = os.path.abspath("templates/static/")
    setup_db(app)
    CORS(app)

    """ uncomment at the first time running the app """
    # db_drop_and_create_all()
    # create a flag to check this

    @app.route('/', methods=['GET'])
    def index():
        try:
            all_users = User.query.order_by(User.full_name).all()
            users = []
            users = [y.full_name for y in all_users]
            all_foods = Food.query.order_by(Food.title).all()
            foods = []
            foods = [z.title for z in all_foods]
            return render_template('/layouts/index.html', user_rows=users, menu_rows=foods), 200
        except:
            abort(500)

    @app.route("/process", methods=['POST'])
    def process_order():
        request_id = uuid.uuid1()
        print("Generated request ID: %s" % request_id)
        if "name" and "menu" in request.form:
            obj = Order(request.form['name'], request.form['menu'])
            try:
                process_order = Order.insert(obj)
            except IntegrityError as e:
                """
                Preventing the a user from making duplicate orders, handled by unique constraint in the DB table
                """
                error = str(e.__dict__['orig'])
                print(error)
                return jsonify({"error": "Oops. You've already ordered before!"})
            else:
                return jsonify({"name" : "Hooray. Order successfully placed"})
            finally:
                print("Workflow completed for request ID: %s" % request_id)


    @app.route("/director", methods=['GET'])
    def director():
        return render_template("director.html")


    @app.route("/director/user_administration", methods=['GET'])
    def view_user_administration():
        users = User.query.all()
        return render_template("user_administration.html", user_data=users)


    @app.route("/director/menu_administration", methods=['GET'])
    def view_menu_administration():
        foods = Food.query.all()
        return render_template("menu_administration.html", food_data=foods)


    @app.route("/director/pending_orders", methods=['GET'])
    def view_pending_orders():
        all_orders = Order.query.all()
        orders = []
        orders = [x for x in all_orders]

        query_count_orders = Order.group_orders(all_orders)
        count_orders = []
        count_orders = [c for c in query_count_orders]
        return render_template("pending_orders.html", order_rows=orders, food_orders=count_orders);


    @app.route("/add_menu_item", methods=['POST'])
    def add_menu_item():
        date_now = datetime.now()
        date_time = date_now.strftime("%d/%m/%Y")
        obj = Food(request.form['title'], date_time)
        try:
            Food.insert(obj)
        except SQLAlchemyError as exc:
            print(exc)
            return jsonify({"error": "Error occurred when attempting to add menu item"})
        else:
            return jsonify({"name": "Menu item successfully added - Reloading"})


    @app.route("/delete_all_menu_items", methods=['POST'])
    def delete_all_menu_items():
        try:
            obj = Food.query.all()
            for item in obj:
                Food.delete(item)
        except SQLAlchemyError as exc:
            print(exc)
            return jsonify({"error": "Unable to delete all items"})
        else:
            return jsonify({"name": "All items successfully deleted - Reloading in 5 seconds"})


    @app.route('/delete_menu_item', methods=['POST'])
    def delete_menu_item():
        record_id = request.form['itemid']
        try:
            obj = Food.query.filter(Food.id == record_id)
            for item in obj:
                Food.delete(item)
        except:
            return jsonify({"error": "Unable to delete record"})
        else:
            return jsonify({"name": "Successfully deleted record"})


    @app.route("/add_user", methods=['POST'])
    def add_user():
        full_name = request.form['full_name']
        email_address = request.form['email_address']
        phone_number = request.form['phone_number']
        obj = User(full_name, email_address, phone_number)
        try:
            User.insert(obj)
        except SQLAlchemyError as exc:
            print(exc)
            return jsonify({"error": "Error occurred when attempting to add user"})
        else:
            return jsonify({"name": "User successfully added - Reloading"})

    @app.route('/delete_user', methods=['POST'])
    def delete_user():
        record_id = request.form['userid']
        try:
            obj = User.query.filter(User.id == record_id)
            for user in obj:
                User.delete(user)
        except:
            return jsonify({"error": "Unable to delete record"})
        else:
            return jsonify({"name": "Successfully deleted record"})


    @app.route('/delete_all_users', methods=['POST'])
    def delete_all_users():
        try:
            obj = User.query.all()
            for usr in obj:
                User.delete(usr)
        except SQLAlchemyError as exc:
            print(exc)
            return jsonify({"error": "Unable to delete all users"})
        else:
            return jsonify({"name": "All users successfully deleted - Reloading in 5 seconds"})

    @app.route('/get_customer_by_id', methods=['POST'])
    def get_customer_by_id():
        customer_id = request.form['customer_id']
        print(customer_id)
        customer = User.query.get(customer_id)
        print(customer)
        print(customer.as_dict())
        print(User.as_dict())


    @app.route('/remove_pending_orders')
    def remove_pending_orders():
        try:
            obj = Order.query.all()
            for order in obj:
                Order.delete(order)
        except SQLAlchemyError as exc:
            print(exc)
        return '', 200

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Server Error. Check server logs!"
        }), 500

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='127.0.0.1', port=port, debug=True)
