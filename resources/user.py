from flask_restful import Resource, reqparse
from models.userModel import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST


class User(Resource):

    #ATRIBUTOS DA CLASSE
    arguments = reqparse.RequestParser()
    #Indenpendente do que for passado no JSON,
    #seram utilizados apenas os itens listados
    arguments.add_argument("id")
    arguments.add_argument("name", type=str, required=True,
                           help="'name' field can't be blank")
    arguments.add_argument("username", type=str, required=True,
                           help="'username' field can't be blank")
    arguments.add_argument("password", type=str, required=True,
                           help="'password' field can't be blank")

    #METODO GET = obtem os dados

    def get(self):
        data = User.arguments.parse_args()
        user = UserModel.findByUsername(data["username"])
        if user:
            return user.json(), 200
        else:
            return {"message": "user not found"}

    #METODO POST = adiciona um dado
    def post(self):
        data = User.arguments.parse_args()
        if UserModel.findByUsername(data["username"]):
            return {"message": "User already exists"}, 400

        newUser = UserModel(**data)
        #Tratamento de excecoes
        try:
            UserModel.save(newUser)
            return {"message": "New user added successfully", "user": newUser.json()}, 201

        except Exception as e:
            return {"message": "'{}'".format(e), "user": newUser.json()}, 500

    #METODO PUT = atualiza um dado

    @jwt_required()
    def put(self):
        data = User.arguments.parse_args()
        user = UserModel.findByUsername(data["username"])

        if user:
            #Tratamento de excecoes
            try:
                user.update(**data)
                return {"message": "Updated successfully!", "user": user.json()}, 200
            except Exception as e:
                return {"message": "'{}'".format(e), "user": user.json()}, 500

        else:
            newUser = UserModel(**data)
            try:
                UserModel.save(newUser)
                return {"message": "Created successfully!", "user": newUser.json()}, 201

            except Exception as e:
                return {"message": "'{}'".format(e), "user": newUser.json()}, 500

    #METODO DELETE = deleta um dado
    @jwt_required()
    def delete(self):
        data = User.arguments.parse_args()
        user = UserModel.findById(data["user_id"])
        if user:
            #Tratamento de excecoes
            try:
                user.delete()
                return {"message": "User deleted!"}

            except Exception as e:
                return {"message": "'{}'".format(e), "user": user.json()}, 500

        else:
            return {"message": "User doesn't exists"}


class UserList(Resource):
    @jwt_required()
    def get(self):
        return {"Users": [user.json() for user in UserModel.query.all()]}


class UserLogin(Resource):

    arguments = reqparse.RequestParser()
    arguments.add_argument("username", type=str, required=True,
                           help="'username' field can't be blank")
    arguments.add_argument("password", type=str, required=True,
                           help="'password' field can't be blank")

    @classmethod
    def post(self):
        data = UserLogin.arguments.parse_args()
        user = UserModel.findByUsername(data["username"])

        if user and safe_str_cmp(user.password, data["password"]):
            accessToken = create_access_token(identity=user.id)
            return {"token": accessToken, "user": user.json()}, 200
        else:
            return {"message": "Error! Please, verify your login informations."}, 400


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        token = get_jwt()['jti']  # JWT Token Identifier
        BLACKLIST.add(token)
        return {"message": "You were logged out"}
