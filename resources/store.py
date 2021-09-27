from flask_restful import Resource, reqparse
from models.store import StoreModel

class Store(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True, help="This field cannot be blank!")


    def get(self, name):
        try:
            store = StoreModel.find_by_name(name)
            if store:
                return store.json()
            return {"message": "Store not found"}, 404
        except:
            return {"message": "Error occured while searching the table!"}, 500
        
    
    def post(self):
        pl = Store.parser.parse_args()
        try:
            if StoreModel.find_by_name(pl["name"]):
                return {"message": "Store already present"}, 400
            new_store = StoreModel(pl["name"])
            new_store.save_to_db()
            return new_store.json(), 201
        except:
            return {"message": "Error occured while creating the store!"}, 500


    def delete(self, name):
        try:
            existing_store = StoreModel.find_by_name(name)
            if existing_store:
                existing_store.delete_from_db()
                return {"message": "Store deleted!"}
        except:
            return {"message": "Error occured while searching the table!"}, 500

class StoreList(Resource):

    def get(self):
        stores = StoreModel.return_all_stores()
        return {"stores": stores}
