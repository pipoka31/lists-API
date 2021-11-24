from sql_alchemy import database
from models.userModel import UserModel

class ListModel(database.Model):
    __tablename__ = "lists"

    id = database.Column(database.Integer(), primary_key = True)
    name = database.Column(database.String())
    is_notebook = database.Column(database.Integer(), default=0)
    color = database.Column(database.String())
    user_id = database.Column(database.Integer(), database.ForeignKey("users.id"))
    favorite = database.Column(database.Integer(), default=0)
    items = database.relationship("ItemModel")#Lista de "items"

    def __init__(self,id,name,user_id, is_notebook, color):
        self.name = name
        self.is_notebook = is_notebook
        self.color = color
        self.user_id = user_id

    def json(self):
        notebook = False
        if self.is_notebook == 1:
            notebook = True
        return {
        "id": self.id,
        "is_notebook": self.is_notebook,
        "color": self.color,
        "favorite": self.favorite,
        "name": self.name,
        "user_id": self.user_id,
        "items_quantity": len(self.items),
        "items": [ item.json() for item in self.items ]
        }

    #Encontra list a partir do ID
    @classmethod
    def findById(cls,list_id):
        list = cls.query.filter_by(id = list_id).first()#Faz uma busca e retorna a primeira ocorrência
        if list:
            return list
        else:
            return None

    @classmethod
    def findByListname(cls,list_name):
        list = cls.query.filter_by(name = list_name).first()
        if list:
            return list
        else:
            return None

    #Salva o item no database
    def save(self):
        if not UserModel.findById(self.user_id):
            return { "message": "The associated user doesn't exists" }, 400

        database.session.add(self)
        database.session.commit()

    #Atualiza a list no database
    def update(self,name):
        self.name = name
        ListModel.save(self)


    #Deleta uma list no database
    def delete(self):
        [item.delete() for item in self.items ]#Deleta os itens associados a lista
        database.session.delete(self)
        database.session.commit()
