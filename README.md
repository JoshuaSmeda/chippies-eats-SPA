# chippies_ordering_system

We South Africans love chippies! Take the hard work out of ordering in bulk today!

http://www.eatout.co.za/venue/chippies-prego-rondebosch/

![final](https://user-images.githubusercontent.com/39983886/117582703-99e6f380-b103-11eb-9ace-b65cd7bd9fc6.png)

# chippies_ordering_system

Takes the hard work out of chippies orders using this simple web based SPA.

# Notes

This code base is in dire need of refactoring. I just pumped this out and didn't actually write pythonically :(

# Example Nginx configuration to serve SPA 

```
server {
  listen [::]:80 default_server;
  server_name chippies.server.com;

  location / { 
    proxy_pass http://localhost:5000;
  }

  location /admin_panel {
    proxy_pass http://localhost:5000;
    auth_basic "Restricted Content";
    auth_basic_user_file /etc/nginx/.htpasswd; # For admin interface in SPA
  }
}
```

# Example menu:
```
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
  
```


Step 1.

Init heroku app
Create build - heroku buildpacks:set heroku/python

