import os
import uuid
from flask import Flask, request, abort, jsonify, render_template
from flask_cors import CORS
from models import setup_db, Food, Order, User, db_drop_and_create_all

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

    @app.route("/admin_panel", methods=['GET'])
    def admin_panel():
        return render_template("/layouts/admin_panel.html")

    @app.route("/test", methods=['POST', 'GET'])
    def test_menu():
        users = User.query.all()
        return render_template("test.html", user_data=users)

    @app.route('/adc', methods=['POST'])
    def test():
        print(request.headers)
        print(request)
        print(request.data)
        return 'test'
 
    @app.route('/food')
    def get_food():
        try:
            foods = Food.query.order_by(Food.created_date).all()
            food = []
            food = [x.created_date for x in foods]
            return jsonify(
                    {
                        "success": True,
                        "food name": food
                    }
            ), 200
        except:
            abort(500)

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Server Error"
        }), 500

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='127.0.0.1', port=port, debug=True)
