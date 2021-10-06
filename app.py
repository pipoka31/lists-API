from flask import Flask, jsonify
from flask_restful import Api
from resources.marketList import MarketItem, MarketList
from resources.user import User, UserList, UserLogin, UserLogout
from resources.list import Lists, List
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from flask_cors import CORS

#Gera a chave secreta do app


def key():
    list = ""
    for number in range(0, 100, 2):
        list = list + chr(number)
    return "Abc" + list + "xyZ"


#Configuracoes do inicio
app = Flask(__name__)
cors = CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = key()
app.config["JWT_BLACKLIST_ENABLED"] = True
api = Api(app)
jwt = JWTManager(app)  # Integra o JWT ao app

#Routes

api.add_resource(MarketItem, "/item")
api.add_resource(MarketList, "/allitems")  # Mostra todos os itens

api.add_resource(User, "/user")
api.add_resource(UserList, "/userlist")  # Mostra todos os itens
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")

api.add_resource(Lists, "/lists/<int:user_id>")
api.add_resource(List, "/list")


@app.before_first_request
def createDatabase():
    database.create_all()

#Verifica se o token esta na Blacklist


@jwt.token_in_blocklist_loader
def verifyBlacklist(self, token):
    return token["jti"] in BLACKLIST


@jwt.revoked_token_loader
def invalidAccessToken(jwt_header, jwt_payload):
    return jsonify({"message": "You have been logged out"}), 401


if __name__ == '__main__':
    from sql_alchemy import database
    database.init_app(app)
    app.run(host="127.0.0.1", port=5000,debug=True)
