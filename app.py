import os
import re

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from models.blacklist import TokenBlacklist

from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db


app = Flask(__name__)
app.secret_key = 'koopa'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

uri = os.getenv('DATABASE_URL', 'sqlite:///data.db')
if uri.startswith('postgres://'):
    uri = uri.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

jwt = JWTManager(app)
    
@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blocklist_loader
def check_if_user_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token = TokenBlacklist.find_by_jti(jti)
    return token is not None

@jwt.revoked_token_loader
def token_revode_callback(jwt_header, jwt_payload):
    return {
        'description': 'The token has been revoked',
        'error': 'token_revoked'
    }, 401
    
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)