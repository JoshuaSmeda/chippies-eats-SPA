import os, uuid, simplejson, json
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
    #fn = 'flush_and_create_db.file'
    #if os.path.isfile(fn):
    #    print("Not flushing and creating databases since '%s' exists. If this is a new instance, ensure this file doesn't exist" % fn)
    #else:
    db_drop_and_create_all()
    #    os.mknod(fn)

    #create a flag to check this

    @app.route('/', methods=['GET'])
    def index():
        try:
            all_users = User.query.order_by(User.full_name).all()
            users = []
            users = [y.full_name for y in all_users]
            all_foods = Food.query.order_by(Food.title).all()
            foods = []
            foods = [z.title for z in all_foods]
            return render_template('index.html', user_rows=users, menu_rows=foods), 200
        except Exception as error:
            print(error)
            abort(500)

    @app.route("/process", methods=['POST'])
    def process_order():
        request_id = uuid.uuid1()
        print("Generated request ID: %s" % request_id)
        if "name" and "menu" in request.form:
            obj = Order(request.form['name'], request.form['menu'])
            try:
                process_order = Order.insert(obj)
            except IntegrityError as exc:
                """
                Preventing the a user from making duplicate orders, handled by unique constraint in the DB table
                """
                error = str(exc.__dict__['orig'])
                print(error)
                return jsonify({"error": "Oops! You've already ordered before :<"})
            else:
                return jsonify({"name" : "Hooray! Order successfully placed :>"})
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
        obj = Food(request.form['title'], date_now)
        try:
            Food.insert(obj)
        except SQLAlchemyError as exc:
            error = str(exc.__dict__['orig'])
            return jsonify({"error": "Oops! %s" % error})
        else:
            return jsonify({"name": "Menu item successfully added - Reloading"})


    @app.route("/delete_all_menu_items", methods=['POST'])
    def delete_all_menu_items():
        try:
            obj = Food.query.all()
            for item in obj:
                Food.delete(item)
        except SQLAlchemyError as exc:
            error = str(exc.__dict__['orig'])
            return jsonify({"error": "Oops! %s" % error})
        else:
            return jsonify({"name": "All items successfully deleted - Reloading in 5 seconds"})


    @app.route('/delete_menu_item', methods=['POST'])
    def delete_menu_item():
        record_id = request.form['itemid']
        try:
            obj = Food.query.filter(Food.id == record_id)
            for item in obj:
                Food.delete(item)
        except SQLAlchemyError as exc:
            error = str(exc.__dict__['orig'])
            return jsonify({"error": "Oops! %s" % error})
        else:
            return jsonify({"name": "Successfully deleted record"})


    @app.route("/add_user", methods=['POST'])
    def add_user():
        full_name = request.form['full_name']
        email_address = request.form['email_address']
        cellphone_number = request.form['cellphone_number']
        obj = User(full_name, email_address, cellphone_number)
        try:
            User.insert(obj)
        except SQLAlchemyError as exc:
            error = str(exc.__dict__['orig'])
            return jsonify({"error": "Oops! %s" % error})
        else:
            return jsonify({"name": "User successfully added - Reloading"})

    @app.route('/delete_user', methods=['POST'])
    def delete_user():
        record_id = request.form['userid']
        try:
            obj = User.query.filter(User.id == record_id)
            for user in obj:
                User.delete(user)
        except SQLAlchemyError as exc:
            error = str(exc.__dict__['orig'])
            return jsonify({"error": "Oops! %s" % error})
        else:
            return jsonify({"name": "Successfully deleted record"})


    @app.route('/delete_all_users', methods=['POST'])
    def delete_all_users():
        try:
            obj = User.query.all()
            for usr in obj:
                User.delete(usr)
        except SQLAlchemyError as exc:
            error = str(exc.__dict__['orig'])
            return jsonify({"error": "Oops! %s" % error})
        else:
            return jsonify({"name": "All users successfully deleted - Reloading in 5 seconds"})

    @app.route('/get_customer_by_id', methods=['POST'])
    def get_customer_by_id():
        customer_id = request.form['customer_id']
        customer = User.query.get(customer_id)
        cust_dict = customer.as_dict()
        json_response = json.dumps(cust_dict)
        return json_response

    @app.route('/update_user_record', methods=['POST'])
    def update_user_record():
        customer_id = request.form['customer_id']
        full_name = request.form['full_name']
        email_address = request.form['email_address']
        cellphone_number = request.form['cellphone_number']
        try:
            obj = User.query.filter(User.id == customer_id).update({"full_name": full_name, "email_address": email_address, "cellphone_number": cellphone_number})
            User.update(obj)
        except SQLAlchemyError as exc:
            error = str(exc.__dict__['orig'])
            return jsonify({"error": "Oops. %s" % error})
        else:
            return jsonify({"name": "Record successfully edited. Refreshing!"})


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
        print(error)
        return jsonify({
            "success": False,
            "error": 500,
            "message": str(error)
        }), 500

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='127.0.0.1', port=port, debug=True)
