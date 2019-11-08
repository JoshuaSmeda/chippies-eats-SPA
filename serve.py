#!/usr/bin/python3

import sqlite3
import os
from flask import *
from waitress import serve

app = Flask(__name__)
app._static_folder = os.path.abspath("templates/static/")

class setup_datastores:
  def __init__(self, datastore_name):
    self.datastore_name = datastore_name

#  def create_datastore(self):
#    if not self.datastore_name:
##      print("No datastores supplied - please recheck config.py")
#    else:
#      for name in self.datastore_name:
#        try:
#          sqlite3.connect(name)
##        except Exception as e:
#          print("Error when creating datastores: % " % str(e))
#          quit()

#setup = setup_datastores(['user.db', 'food.db', 'order.db'])
#setup.create_datastore()

user_db = sqlite3.connect('user.db')
food_db = sqlite3.connect('food.db')
order_db = sqlite3.connect('order.db')

try:
  user_db.execute("create table Users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)")
  print("User Table created successfully")
  user_db.close()
except sqlite3.OperationalError as e:
  print("Hangup - " + str(e))

try:
  food_db.execute("create table Food (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NO NULL)")
  print("Food Table created successfully")
  food_db.close()
except sqlite3.OperationalError as e:
  print("Hangup - " + str(e))

try:
  order_db.execute("create table Orders (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NO NULL, menu TEXT NO NULL)")
  print("Order Table created successfully")
  order_db.close()
except sqlite3.OperationalError as e:
  print("Hangup - " + str(e))

@app.route("/")
def index():
    user_con = sqlite3.connect("user.db")
    user_con.row_factory = sqlite3.Row
    user_cur = user_con.cursor()
    user_cur.execute("select * from Users")
    user_rows = user_cur.fetchall()
    menu_con = sqlite3.connect("food.db")
    menu_con.row_factory = sqlite3.Row
    menu_cur = menu_con.cursor()
    menu_cur.execute("select * from Food")
    menu_rows = menu_cur.fetchall()
    return render_template("/layouts/index.html", user_rows=user_rows, menu_rows=menu_rows);

@app.route("/view_user")
def view_user():
    con = sqlite3.connect("user.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Users")
    rows = cur.fetchall()
    return render_template("view_user.html", rows=rows);

@app.route("/view_menu")
def view_menu():
    con = sqlite3.connect("food.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Food")
    rows = cur.fetchall()
    return render_template("view_menu.html", rows=rows);

@app.route("/view_order")
def view_order():
    order_con = sqlite3.connect("order.db")
    order_con.row_factory = sqlite3.Row
    order_cur = order_con.cursor()
    order_cur.execute("select * from Orders")
    order_rows = order_cur.fetchall()

    calculate_con = sqlite3.connect("order.db")
    calculate_con.row_factory = sqlite3.Row
    calculate_cur = calculate_con.cursor()
    calculate_cur.execute("SELECT menu, COUNT(menu) FROM Orders GROUP BY menu")
    calculate_rows = calculate_cur.fetchall()
    return render_template("view_order.html", order_rows=order_rows, calculate_rows=calculate_rows);


@app.route("/add_user")
def add_user():
    return render_template("add_user.html")

@app.route("/add_menu")
def add_menu():
    return render_template("add_menu.html")

@app.route("/delete_user")
def delete_user():
    return render_template("delete_user.html")

@app.route("/delete_success_user", methods = ["POST"])
def delete_user_success():
    id = request.form["id"]
    with sqlite3.connect("user.db") as con:
        try:
            cur = con.cursor()
            cur.execute("DELETE from Users where id=?", (id, ))
            msg = "Successfully deleted user"
        except Exception as e:
            print("error " + str(e))
            msg = "Unable to delete"
        finally:
            return render_template("delete_success_user.html", msg = msg)

@app.route("/delete_menu")
def delete_menu():
    return render_template("delete_menu.html")

@app.route("/delete_success_menu", methods = ["POST"])
def delete_menu_success():
    id = request.form["id"]
    with sqlite3.connect("food.db") as con:
        try:
            cur = con.cursor()
            cur.execute("DELETE FROM Food WHERE id = ?", (id, ))
            msg = "Successfully deleted menu item"
        except Exception as e:
            print("error " + str(e))
            msg = "Unable to delete"
        finally:
            return render_template("delete_success_menu.html", msg = msg)


@app.route("/admin_panel")
def AdminPanel():
  return render_template("/layouts/admin_panel.html")

@app.route("/process", methods=['POST'])
def process():
  name = request.form['name']
  menu = request.form['menu']
  order_con = sqlite3.connect("order.db")
  print("Name: " + name + " Menu: " + menu)
  if request.method == "POST":
    if name and menu:
      cur = order_con.cursor()
      cur.execute("""SELECT name, menu FROM Orders WHERE name=? AND menu=?""", (name, menu))
      result = cur.fetchone()
      if result:
        print("Result Found")
        return jsonify({'error' : 'Oops. You already submitted today!'})
      else:
        try:
          with sqlite3.connect("order.db") as con:
            success_msg = "Order Successfully Placed"
            cur = con.cursor()
            cur.execute('INSERT INTO Orders (name, menu) VALUES(?,?)', [name, menu])
            con.commit()
            return jsonify({'name' : success_msg})

        except Exception as e:
          con.rollback()
          print("error " + str(e))
          msg = "Unable to add user's order to DB"

@app.route("/addmenuitem",methods = ["POST","GET"])
def AddMenuItem():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["name"]
            with sqlite3.connect("food.db") as con:
                cur = con.cursor()
                cur.execute('INSERT INTO Food (name) VALUES(?)', [name])
                con.commit()
                msg = "Menu Item successfully Added"
        except Exception as e:
            con.rollback()
            print("error " + str(e))
            msg = "We can not add the menu item to the DB"
        finally:
            return render_template("success.html",msg = msg)
            con.close()

@app.route("/adduser",methods = ["POST","GET"])
def AddUser():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["name"]
            with sqlite3.connect("user.db") as con:
                cur = con.cursor()
                cur.execute('INSERT INTO Users (name) VALUES(?)', [name])
                con.commit()
                msg = "User successfully Added"
        except Exception as e:
            con.rollback()
            print("error " + str(e))
            msg = "We can not add the user to the DB"
        finally:
            return render_template("success.html",msg = msg)
            con.close()

@app.route("/submitdetails", methods = ["POST","GET"])
def Submit_Details():
    msg = "was successfull"
    return render_template("success.html", msg = msg)

if __name__ == "__main__":
#   app.run(debug=True) ## Replaced by Waitress
     serve(app, host='127.0.0.1', port=5000)

#
