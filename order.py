import re
from collections import Counter
from datetime import datetime, timedelta, time, date
import logging
import logging.handlers
import os
import collections

global ChippiesMenu
ChippiesMenu = [ "Chicken Prego Roll with chips", "Chicken BBQ Roll with chips", "Steak Prego Roll with chips", "Steak BBQ Roll with chips", "BBQ Chip Roll", "Chip Roll with S & V", "Prego Steak Roll, B & C with chips", "BBQ Steak Roll, B & C with chips" ]
OrderList = []
global d
running = True
log = logging.getLogger(__name__)
log.root.setLevel(logging.DEBUG)
log_formatter = logging.Formatter('%(levelname)s %(message)s')
log_handler = logging.StreamHandler()
log_handler.setFormatter(log_formatter)
log.addHandler(log_handler)
d = {}

def dict_creator(staff_name, str_order):
  d[staff_name] = str_order
  print ""
  print("CURRENT ORDER LIST:")
  for key, value in d.items():
    print(key + " " + value)

def get_log_date_log():
  date = datetime.now()
  dt_log = date.strftime("%Y-%m-%d %H:%M:%S")
  return dt_log

def get_log_date_file():
  date = datetime.now()
  dt_file = date.strftime("%Y-%m-%d")
  return dt_file

def write_file(file_name, data_to_write):
  try:
    with open(file_name, 'a') as f:
      f.write(data_to_write.encode('utf-8'))
      f.write("\n")
  except Exception as error:
    log.error('Error writing file ' + file_name + '. Cannot continue. Exception: ' + str(error))
    quit()

def log_order(response):
  current_dt = get_log_date_file()
  global file_name
  file_name = 'order-' + current_dt
  write_file(os.path.join(file_name), response)

def order_total_counting():
  global c
  c = collections.Counter(OrderList)
  for key, value in c.items():
    print(key, value)
    formatted = key + " " + str(value)
    log_order(formatted)


current_dt = get_log_date_file()
try:
  if os.stat("order-" + current_dt).st_size == 0:
    pass
  else:
    print("File: order-" + current_dt + " exists.")
    confirmation = raw_input("Y - Do you want to remove the existing order / N - Append to existing order: ")
    confirmation = confirmation.upper()
    if confirmation == "Y":
      os.remove("order-" + current_dt)
except Exception, e:
  pass # Hiding this

def details():
  while running == True:
    global staff_name
    staff_name = raw_input("Name: ")
    if not re.match("^[a-zA-Z ]*$", staff_name):
      print("Please use letters only")
    elif len(staff_name) == 0:
      print("Please enter a valid input")
    else:
      staff_name = staff_name.title()
      break

details()

def print_menu():
  print ("""
  -----------------------------------------------
  |               CHIPPIES MENU                 |
  |                                             |
  |  -----------------------------------------  |
  |  1. Chicken Prego Roll with chips           |
  |  2. Chicken BBQ Roll with chips             |
  |  3. Steak Prego Roll with chips             |
  |  4. Steak BBQ Roll with chips               |
  |  5. BBQ Chip Roll                           |
  |  6. Chip Roll with S & V                    |
  |  7. Prego steak Roll, B & C with chips      |
  |  8. BBQ steak Roll, B & C with chips        |
  -----------------------------------------------
  """)

print_menu()

def Menu_Choice():
  global str_order
  global customerOrder
  while True:
      try:
        chippies_kind = int(raw_input("Choice of Chippies:"))
        if chippies_kind < 1:
          print("Refer to Chippies Menu for Chippies number")
          continue
        if chippies_kind > 8:
          print("Refer to Chippies Menu for Chippies number")
          continue
        else:
          chippies = chippies_kind - 1
          customerOrder = ChippiesMenu[chippies]
          print(customerOrder)
          str_order = ''.join(customerOrder) ## Converts from list to string so it looks pretty :)
          break
      except ValueError:
        print("Please use numbers only")
        continue

Menu_Choice()

def customerDetails():
  print ("")
  print ("CUSTOMER and ORDER DETAILS")
  print ("")
  print ("Name: "), staff_name
  print ("ORDER: "), customerOrder
customerDetails()

print ("")

def confirm():
  confirmation = raw_input("Y - confirm order / N - cancel order:")
  confirmation = confirmation.upper()
  if confirmation == "Y":
    print("DETAILS CONFIRMED")
    dict_creator(staff_name, str_order)
  elif confirmation == "N":
    print("DETAILS CANCELLED - order has been reset")
    print_menu()
    Menu_Choice()
    customerDetails()
    confirm()
  else:
    print("Please enter Y or N")
    confirm()

confirm()

print ("")

def order_some_more():
  while running == True:
    order_more = raw_input("Z - order more / X - exit program:")
    order_more = order_more.upper()
    if order_more == "Z":
      details()
      print_menu()
      Menu_Choice()
      customerDetails()
      confirm()
    elif order_more == "X":
      print ("")
      print ("ORDER COMPLETED - PRINTING BELOW:")
      for key, value in d.items():
        order_list = ("Person: " + key + " Order: " + value)
        print(order_list)
        formatted_order_list = (key + " " + value)
        log_order(formatted_order_list)
        OrderList.append(value)
      break
    else:
      print ("Please enter X or Z")
      order_some_more()

order_some_more()
print("\n" + "CALCULATING ORDER TOTALS:")
log_order("")
order_total_counting()
