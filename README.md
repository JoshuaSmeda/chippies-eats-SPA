# ChippiesEats - Single page Application (Web)

We South Africans love ordering food. Take the hard work out of ordering in bulk today, let **ChippiesEats** handle it for you!

## Preview
![final](https://user-images.githubusercontent.com/39983886/117582703-99e6f380-b103-11eb-9ace-b65cd7bd9fc6.png)

## Live web example
https://chippies-eats.herokuapp.com/

# Tech stack
- Python
- Jquery (Ajax)
- Bootstrap
- Postgresql
- Heroku

## Overview

There is a administration panel that allows a administrator to add food items, users and view a comprehensive and cumulative list of pending orders

#### Director (Administration Panel)
![admin_panel](https://user-images.githubusercontent.com/39983886/119234188-d6b3e100-bb2c-11eb-89aa-61ad29cedefa.png)

#### Pending orders
![pending_orders](https://user-images.githubusercontent.com/39983886/119234222-0bc03380-bb2d-11eb-8fd2-f2c8de109279.png)


### Ordering

A user can only place one order before the database record must be deleted. A successful order will appear as follows:
![order_placed](https://user-images.githubusercontent.com/39983886/119234290-5e015480-bb2d-11eb-96e3-c7a9f47c1241.png)

While a unsuccessful order will appears as follows: <br>
![Ordered_before](https://user-images.githubusercontent.com/39983886/119234282-5641b000-bb2d-11eb-975f-9bc8bad5415c.png)


### Example Nginx configuration (Reverse Proxy)

1. `pip3 install -r requirements.txt`
2. `python3 app.py`
3. Use the following Nginx configuration as a guideline:

```
server {
  listen [::]:80 default_server;
  server_name subdomain.domain.tld;

  location / { 
    proxy_pass http://localhost:5000;
  }

  location /director {
    proxy_pass http://localhost:5000;
    auth_basic "Restricted Content";
    auth_basic_user_file /etc/nginx/.htpasswd; # Protected admin route
  }
}

```
### Example Gunicorn webserver deployment
1. `pip3 install -r requirements.txt`
2. `gunicorn app:app`

## Helpful hints

If you have a number of pending orders you want to flush, you can perform a **GET** request to the following endpoint to flush all pending orders:

`/remove_pending_orders`


## Legal 
If there is any copyright infrightment or you would like me to take this down, please reach out to me via Linkedin or my email address and I'll gladly do so!
