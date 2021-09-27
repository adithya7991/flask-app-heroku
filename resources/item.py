
from flask import request
from flask_restful import Resource
from flask_jwt import jwt_required
from utilities import *
from models.item import ItemModel



class Item(Resource):

    @jwt_required()
    def get(self, name):

        try:
            item = ItemModel.find_by_name(name)
        except Exception as e:
            print(str(e))
            return {"message": "Error occured while searching the table!"}, 500

        if item:
            return item.json(), 200
        return {"message": "Item not found!"}, 404

    @Utilities.check_content_type_and_body_for_post
    @jwt_required()
    def post(self): # Creates record if not exists else 4xx error

        # pl = request.get_json()
        pl = Utilities.reqparser(request)
        
        # Check already exists; since GET and POST has jwt_req(), they call each other, else use classMethod
        try:
            item = ItemModel.find_by_name(pl["name"])
        except:
            return {"message": "Error occured while searching the table!"}, 500  
                          
        if item:            
            return {"message": "Item already exists"}, 400
        else:  
            new_item = ItemModel(**pl)  
            try:     
                new_item.save_to_db()
            except:
                return {"message": "Error occured while inserting the record!"}, 500   
            return new_item.json(), 201

    @jwt_required()
    def delete(self, name):
        
        item = ItemModel.find_by_name(name)
        if item:
            try:
                item.delete_from_db()
                return {"message": "Item deleted successfully!"} 
            except:
                return {"message": "Error occured while deleting the record!"}, 500              
            
        return {"message": "Item not found"}, 400

    @Utilities.check_content_type_and_body_for_put
    @jwt_required()
    def put(self, name): # creates record if not exists else update the record
        
        # pl = request.get_json()    
        pl = Utilities.reqparser(request)

        try:
            item = ItemModel.find_by_name(name)
        except:
            return {"message": "Error occured while performing SQL operation!"}, 500

        
        if item is None:            
            try:   
                item = ItemModel(name, **pl) 
                item.save_to_db()                 
            except:
                return {"message": "Error occured while inserting the record!"}, 500                      
            return item.json(), 201

        else:
            try:
                item.price = pl["price"]
                item.store_id = pl["store_id"]
                item.save_to_db()
            except:
                return {"message": "Error occured while updating the record!"}, 500
            return item.json()

   

class ItemList(Resource):

    @jwt_required()
    def get(self):           
        item_list = ItemModel.return_all_items()
        return { "items": item_list}