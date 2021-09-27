from flask_restful import reqparse
from flask import request
import sqlite3


class Utilities:
    
    def reqparser(req):
        parser = reqparse.RequestParser()

        if req.method == "POST":
            parser.add_argument('name', type=str, required=True, help="This field cannot be blank!")
        parser.add_argument('price', type=float, required=True, help="This field cannot be blank!")
        parser.add_argument('store_id', type=int, required=True, help="Every item needs a store id!")

        return parser.parse_args()

    # reqparse can handle errors in payload; created for knowledge purpose
    def check_content_type_and_body_for_post(func): # POST
    
        def inner(self):
            ct = request.headers.get('Content-Type')
            pl = request.get_json()        

            if ct != "application/json" or ct == None:
                return {"message": "Operation failed due to improper content type"}, 406
            elif not isinstance(pl,dict):
                return {"message": "Operation failed due to improper JSON body"}, 406        
            else:            
                tup1 = func(self)
                return tup1
    
        return inner
    # reqparse can handle errors in payload; created for knowledge purpose
    def check_content_type_and_body_for_put(func): # PUT
    
        def inner(self, name):
            ct = request.headers.get('Content-Type')
            pl = request.get_json()        

            if ct != "application/json" or ct == None:
                return {"message": "Operation failed due to improper content type"}, 406
            elif not isinstance(pl,dict):
                return {"message": "Operation failed due to improper JSON body"}, 406        
            else:            
                tup1 = func(self, name)
                return tup1
    
        return inner


class DBManager:

    def __init__(self, db):
        self.db = db

    def __enter__(self):
        
        self.cxn = sqlite3.connect(self.db)
        self.cur = self.cxn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.cxn.commit()
        self.cxn.close()