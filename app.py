from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from datetime import timedelta

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "junk1ord"
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


app.config["JWT_AUTH_URL_RULE"] = "/login"
jwt = JWT(app, authenticate, identity)  # /auth


@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify(
        {"access_token": access_token.decode("utf-8"), "user_id": identity.id}
    )


# config JWT to expire within half an hour
app.config["JWT_EXPIRATION_DELTA"] = timedelta(seconds=1800)

api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/item/<string:name>")  # http://127.0.0.1/student/junk1ord
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
