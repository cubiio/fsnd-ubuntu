# Linux Ubuntu Config

## About this project

This is a clone of this project - [GitHub - Item Catalog built with Python Flask](https://github.com/cubiio/fsnd-item_catalog) - hosted on a Linux Ubuntu server with [Amazon LightSail](https://amazonlightsail.com/).

This README includes the following information:

- IP address, URL and ssh details
- Software installed
- Summary of configurations made
- A list of third-party resources used to completed this project


## IP address, URL and ssh details

IP:     107.23.89.190
URL:    [Book Catalogue App](http://107.23.89.190/)

ssh grader@107.23.89.190 -p 22 -i ~/.ssh/udacityLinux

`ssh grader@107.23.89.190 -p 2200 -i ~/.ssh/udacityLinux`



## Software installed

### Ubuntu

[Ubuntu – Ubuntu Packages Search](http://packages.ubuntu.com/)

- Finger
- Apache2
- libapache2-mod-wsgi
- postgresql
- python-psycopg2
- python pip


### Python Packages

```
$ source venv/bin/activate
$ sudo pip install -r requirements.txt
```


```
# file: requirements.txt

appdirs==1.4.0
click==6.7
Flask==0.12
Flask-WTF==0.14.2
itsdangerous==0.24
Jinja2==2.9.4
MarkupSafe==0.23
packaging==16.8
pyparsing==2.1.10
six==1.10.0
SQLAlchemy==1.1.5
Werkzeug==0.11.15
WTForms==2.1
```


And these:

- oauth2client
- requests


## Summary of configurations made

### User configuration

#### Unix

Created `grader` user with `sudo` privileges 

Created `catalog` user

Root user ssh login disabled

#### PostgreSQL

Created `catalog` user, with permissions:

- to login, with password
- to create db

Also, database called catalog created with owner (user) catalog

``` 
# psql

CREATE USER catalog WITH PASSWORD ‘dbpswd’;

ALTER USER catalog CREATEDB;

ALTER ROLE catalog LOGIN;

CREATE DATABASE catalog WITH OWNER catalog;
```


### Update and upgrade packages

Ran these commands to update and upgrade:

```
$ sudo apt-get update

$ sudo apt-get upgrade

```

### Locale

Time set to UTC

Language set to `LANG=en_US.UTF-8` (due to some error messages when trying to install packages)

### Uncomplicated Firewall config

```
To                         Action      From
--                         ------      ----
22                         ALLOW       Anywhere                  
2200/tcp                   ALLOW       Anywhere                  
80/tcp                     ALLOW       Anywhere                  
22 (v6)                    ALLOW       Anywhere (v6)             
2200/tcp (v6)              ALLOW       Anywhere (v6)             
80/tcp (v6)                ALLOW       Anywhere (v6) 
123/tcp (v6)                    ALLOW         Anywhere (v6) 
```


### FlaskApp set-up example code and further configuration

This tutorial is amazing 👍  [How To Deploy a Flask Application on an Ubuntu VPS | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)

**Example directory structure:**

```
|--------FlaskApp
|----------------FlaskApp
|-----------------------static
|-----------------------templates
|-----------------------views
|-----------------------venv
|-----------------------__init__.py
|----------------flaskapp.wsgi
```

For this repo:

- Replace `/fsnd-ubuntu` with `/FlaskApp`
- Replace `/catalog` with `/FlaskApp` i.e. `/FlaskApp/FlaskApp`


**Example code:**

File `__init__.py` in path `/var/www/FlaskApp/FlaskApp`

``` python
# tutorial code
from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello, I love Digital Ocean!"
if __name__ == "__main__":
    app.run()
```

``` python
# My FlaskApp code 
from flask import Flask

from FlaskApp.views.home import homePage
from FlaskApp.views.categories import category_admin
from FlaskApp.views.books import book_admin
from FlaskApp.views.json_api import api_admin
from FlaskApp.views.user_connect import user_admin


app = Flask(__name__)
app.register_blueprint(homePage)
app.register_blueprint(category_admin)
app.register_blueprint(book_admin)
app.register_blueprint(api_admin)
app.register_blueprint(user_admin)

# app.debug = True
if __name__ == "__main__":
    app.run()
```

File and path `/etc/apache2/sites-available/FlaskApp.conf`

- change ServerName to site or IP address
- change ServerAdmin to server admin's email

``` python
<VirtualHost *:80>
        ServerName mywebsite.com
        ServerAdmin admin@mywebsite.com
        WSGIScriptAlias / /var/www/FlaskApp/flaskapp.wsgi
        <Directory /var/www/FlaskApp/FlaskApp/>
            Order allow,deny
            Allow from all
        </Directory>
        Alias /static /var/www/FlaskApp/FlaskApp/static
        <Directory /var/www/FlaskApp/FlaskApp/static/>
            Order allow,deny
            Allow from all
        </Directory>
        ErrorLog ${APACHE_LOG_DIR}/error.log
        LogLevel warn
        CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```


Add file `client_secrets.json` in `/var/www/FlaskApp`:

```
{
    "web": {
        "client_id": "ADD_CLIENT_ID.apps.googleusercontent.com",
        "project_id": "book-catalogue-app",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "ADD_CLIENT_SECRET",
        "redirect_uris": ["ADD_IP_ADDRESS"],
        "javascript_origins": ["ADD_IP_ADDRESS"]
    }
}
```


Amend the password in `database.py` to match that set for the catalog user:

``` python
# Ubuntu, Apache, PostgreSQL config
engine = create_engine(
    'postgresql+psycopg2://catalog:password@localhost/catalog')
```


## Sources of information

- [How To Deploy a Flask Application on an Ubuntu VPS | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)
- [SQLAlchemy - Engines](http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html)
- [How to Configure Ubuntu’s Built-In Firewall](https://www.howtogeek.com/115116/how-to-configure-ubuntus-built-in-firewall/)
- [How to set the timezone on Ubuntu Server](http://www.christopherirish.com/2012/03/21/how-to-set-the-timezone-on-ubuntu-server/)
- [How To Secure PostgreSQL on an Ubuntu VPS | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps)
- [PostgreSQL - Community Help Wiki](https://help.ubuntu.com/community/PostgreSQL)
- [PostgreSQL: Documentation: 9.6: Creating a Database](https://www.postgresql.org/docs/9.6/static/tutorial-createdb.html)
- [PostgreSQL: Documentation: 9.6: Database Roles](https://www.postgresql.org/docs/9.6/static/database-roles.html)
- [PostgreSQL: Documentation: 9.6: Role Attributes](https://www.postgresql.org/docs/9.6/static/role-attributes.html)
- [PostgreSQL by example](http://blog.trackets.com/2013/08/19/postgresql-basics-by-example.html)
- [python - How To Run Postgres locally - Stack Overflow](https://stackoverflow.com/questions/13784340/how-to-run-postgres-locally)
- [postgresql - How to check if a postgres user exists? - Stack Overflow](https://stackoverflow.com/questions/8546759/how-to-check-if-a-postgres-user-exists)
- [Flask - Deploy](http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/)
- [How to disable directory listing in apache? | My Web Experiences](http://www.mywebexperiences.com/2013/05/20/how-to-disable-directory-listing-in-apache/)
- [How To Configure the Apache Web Server on an Ubuntu or Debian VPS | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-configure-the-apache-web-server-on-an-ubuntu-or-debian-vps)
- [Linux directory structure](http://www.thegeekstuff.com/2010/09/linux-file-system-structure)
- [12.04 - How to move one file to a folder using terminal? - Ask Ubuntu](https://askubuntu.com/questions/465877/how-to-move-one-file-to-a-folder-using-terminal#465881)
- [12.04 - How to move one file to a folder using terminal? - Ask Ubuntu](https://askubuntu.com/questions/465877/how-to-move-one-file-to-a-folder-using-terminal#465881)

