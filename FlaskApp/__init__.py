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
