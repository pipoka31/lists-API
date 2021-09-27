from flask_restful import Resource, reqparse
from models.itemModel import ItemModel
from flask_jwt_extended import jwt_required
import sqlite3

class MarketList(Resource):

    pathParams = reqparse.RequestParser()
    pathParams.add_argument("type", type = str)
    pathParams.add_argument("flavor", type = str)


    def get(self):
        connection = sqlite3.connect("Database.db")
        cursor = connection.cursor()
        #Verifica quais parametros nao sao nulos
        data = { key:MarketList.pathParams.parse_args()[key]
        for key in MarketList.pathParams.parse_args()
        if MarketList.pathParams.parse_args()[key] is not None }

        #Define o tipo de busca
        search = ""
        if data.get("type") and data.get("flavor"):
            search = "SELECT * FROM items WHERE type = ? and flavor = ? LIMIT 10"
        elif data.get("type"):
            search = "SELECT * FROM items WHERE type = ? LIMIT 10"
        elif data.get("flavor"):
            search = "SELECT * FROM items WHERE flavor = ? LIMIT 10"
        else:
            search = "SELECT * FROM items"
        values = tuple([data[key] for key in data])
        itemsFromDB = cursor.execute(search,values)

        #Organiza os dados que chegam do banco
        items = []
        for row in itemsFromDB:
             items.append({
             "id": row[0],
             "name": row[1],
             "type": row[2],
             "flavor": row[3],
             "list_id": row[4]
             })
        return {"Items": items}

class MarketItem(Resource):

    #ATRIBUTOS DA CLASSE
    arguments = reqparse.RequestParser()
    #Indenpendente do que for passado no JSON,
    #seram utilizados apenas os itens listados
    arguments.add_argument("name",type=str,required=True,help="'name' field can't be blank")
    arguments.add_argument("type",type=str,required=True,help="'type' field can't be blank")
    arguments.add_argument("flavor")
    arguments.add_argument("list_id",type=str,required=True,help="'list_id' field can't be blank")


    #METODO GET = obtem os dados
    def get(self, item_id):
        item = ItemModel.findById(item_id)
        if item:
            return item.json(), 200
        else:
            return {"message":"item not found"}

    @jwt_required()
    #METODO POST = adiciona um dado
    def post(self):
        data = MarketItem.arguments.parse_args()
        newItem = ItemModel(**data)
        #Tratamento de excecoes
        try:
            newItem.save()
            return {"message":"New item added successfully", "items":newItem.json()}, 201

        except Exception as e:
            return {"message":"'{}'".format(e), "items":newItem.json()}, 500

    @jwt_required()
    #METODO PUT = atualiza um dado
    def put(self, item_id):
        item = ItemModel.findById(item_id)
        data = MarketItem.arguments.parse_args()

        if item:
            #Tratamento de excecoes
            try:
                item.update(**data)
                return {"message": "Updated successfully!", "item": item.json()}, 200
            except Exception as e:
                return {"message": "'{}'".format(e), "item": item.json()}, 500

        else:
            newItem = ItemModel(item_id,**data)
            try:
                ItemModel.save(newItem)
                return {"message": "Created successfully!", "items": newItem.json()}, 201

            except Exception as e:
                return {"message": "'{}'".format(e), "item": item.json()}, 500

    @jwt_required()
    #METODO DELETE = deleta um dado
    def delete(self, item_id):
        item = ItemModel.findById(item_id)
        if item:
            #Tratamento de excecoes
            try:
                item.delete()
                return {"message":"Item deleted!"}

            except Exception as e:
                return {"message": "'{}'".format(e), "item": item.json()}, 500

        else:
            return {"message":"Item doesn't exists"}
