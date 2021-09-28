from datetime import timedelta
from flask import Flask
from flask_restful import  Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import *
from resources.item import *
from resources.store import *
import os



app = Flask(__name__)
api = Api(app)
app.secret_key = "adi"

app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

# Changing to Postgress from SQLite
uri = os.environ.get('DATABASE_URI', 'sqlite:///data.db')
if uri.startswith("postgres://"):
    uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri



# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
jwt = JWT(app, authenticate, identity) # /login , default endpoint name /auth




# START: For displaying pretty JSON in browser
settings = app.config.get('RESTFUL_JSON', {})
settings.setdefault('indent', 2)
settings.setdefault('sort_keys', True)
app.config['RESTFUL_JSON'] = settings
# END

api.add_resource(Item, '/item/<string:name>', '/item')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>', '/store')
api.add_resource(StoreList, '/stores')  




if __name__ == "__main__": # Executed only when run app.py directly
    
    from db import db
    db.init_app(app)

    @app.before_first_request # Before 1st API req, tables will be created
    def create_tables():
        db.create_all()

    app.run(port=5000, debug=True)