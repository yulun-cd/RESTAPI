from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse
from blacklist import TokenBlacklist

from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', 
                          type=str,
                          required=True, 
                          help='Username required!')
_user_parser.add_argument('password', 
                          type=str, 
                          required=True,
                          help='Invalid password!')
    
    
class UserRegister(Resource):    
    def post(self):
        data = _user_parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {'message': 'Username already exists!'}, 400
        
        user = UserModel(**data)
        user.save_to_db()
        
        return {'message': 'User created successfully'}, 201
    

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()
    
    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted'}, 200
    
    
class UserLogin(Resource):    
    def post(self):
        # get data from the parser
        data = _user_parser.parse_args()
        
        # find the user in the database
        user = UserModel.find_by_username(data['username'])
        
        # check the password
        if user and user.password == data['password']:
            # create access token
            access_token = create_access_token(identity=user.id, fresh=True)
            # create refresh token
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
            
        return {'message': 'Invalid credentials'}, 401
    

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        blacklist_token = TokenBlacklist(jti)
        blacklist_token.save_to_db()
        return {'message': 'Successfully logged out.'}, 200
    

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        curr_user = get_jwt_identity()
        new_token = create_access_token(identity=curr_user, fresh=False)
        return {'access_token': new_token}, 200