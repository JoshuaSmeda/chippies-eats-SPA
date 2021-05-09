# chippies_ordering_system

We South Africans love chippies! Take the hard work out of ordering in bulk today!

http://www.eatout.co.za/venue/chippies-prego-rondebosch/

![final](https://user-images.githubusercontent.com/39983886/117582703-99e6f380-b103-11eb-9ace-b65cd7bd9fc6.png)


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


Step 1.

Init heroku app
Create build - heroku buildpacks:set heroku/python

