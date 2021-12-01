from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from flask import jsonify
from models.listModel import ListModel


class Lists(Resource):
    @jwt_required()
    def get(self, user_id):
        return {"lists": [list.json() for list in ListModel.query.filter_by(user_id = user_id)]}


class List(Resource):

    #ATRIBUTOS DA CLASSE
    arguments = reqparse.RequestParser()
    #Indenpendente do que for passado no JSON,
    #seram utilizados apenas os itens listados
    arguments.add_argument("id")
    arguments.add_argument("name",type=str,required=True,help="'name' field can't be blank")
    arguments.add_argument("user_id",required=True,help="'user_id' field can't be blank")
    arguments.add_argument("is_notebook",required=True,help="'is_notebook' field can't be blank")
    arguments.add_argument("color",required=True,help="'color' field can't be blank")

    @jwt_required()
    def get(self):
        list = ListModel.findById(id)
        if list:
            return list.json()
        else:
            return { "message":"List not found" }, 400

    @jwt_required()
    def post(self):
        try:
            data = List.arguments.parse_args()
            newList = ListModel(**data)
            newList.save()
            return { "message": "List created successfully" }, 201
        except Exception as e:
            return {"message": "'{}'".format(e)}

    @jwt_required()
    def put(self, id):
        list = ListModel.findById(id)
        if list:
            try:
                list.update()
                return { "message": "List updated successfully" }, 201
            except Exception as e:
                return e

        else:
            try:
                list.save()
                return { "message": "List created successfully" }, 201
            except Exception as e:
                return { "message": e }, 400

    @jwt_required()
    def delete(self):
        data = List.arguments.parse_args()
        list = ListModel.findById(data["id"])
        if list:
            try:
                list.delete()
                return { "message": "List deleted successfully" }, 200
            except Exception as e:
                return { "message": e }

        else:
            return { "message": "List not found to delete" }, 400
