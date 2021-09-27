
from flask_restful import Resource, reqparse
from utilities import *
from models.user import UserModel



class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="This field cannot be blank!")
    parser.add_argument("password", type=str, required=True, help="This field cannot be blank!")   


    def post(self):

        pl = UserRegister.parser.parse_args()
        # Check for user existence
        if UserModel.find_by_username(pl["username"]):
            return {"message": "User already registered!"}, 400           
        new_user = UserModel(**pl)  
        new_user.save_to_db()     
        return {"message": "User registered successfully!"}, 201


