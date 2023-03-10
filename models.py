from datetime import datetime
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from flask import current_app
from index import db, login_manager
from flask_login import UserMixin
from sqlalchemy import Sequence


# Define a decorator function which takes argument as user_id and return the user for that ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create a class for users, Inheriting from dp.model
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    firstName = db.Column(db.String(100), nullable = False)
    lastName = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(125), unique = True, nullable = False)
    role = db.Column(db.Integer, nullable = False, default = 0)
    password = db.Column(db.String(100), nullable = False)

    # define a method to get a token for reseting the password
    def get_reset_token(self, expires_sec=600):
        s = Serializer(current_app.config['secret_key'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    # define a method to verify the token
    @staticmethod # basically telling to the python, this method is not accepting 'self' as an argument
    def verify_reset_token(token):
        s = Serializer(current_app.config['secret_key'])
        # try to get the user_id from the token
        try:
            user_id = s.loads(token)['user_id']
        except: # if we get an exception 
            return None # when token is invalid or expired
        return User.query.get(user_id) # if we don't get an exception
        


    def __repr__(self):
        return f"User('{self.firstName}', '{self.lastName}', '{self.email}')"
