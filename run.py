from app import app
from db import db

db.init_app(app)

@app.before_first_request # Before 1st API req, tables will be created
def create_tables():
    db.create_all()

