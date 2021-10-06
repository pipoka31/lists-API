from sql_alchemy import database
from models.listModel import ListModel

#MODELO DE UM ITEM
class ItemModel(database.Model):

    #Tabela ao qual esse modelo pertence
    __tablename__ = "items"

    #Define o tipo de campo que sera adicionado ao BD
    id = database.Column(database.Integer(), primary_key = True)
    name = database.Column(database.String(100))
    type = database.Column(database.String(100))
    flavor = database.Column(database.String(100))
    done = database.Column(database.Integer(),default=0)
    list_id = database.Column(database.Integer(), database.ForeignKey("lists.id"))


    def __init__(self,name,type,flavor,list_id):
        self.name = name
        self.type = type
        self.flavor = flavor
        self.list_id = list_id


    def json(self):
        done = False
        if self.done == 1:
            done = True
        return {
        "id": self.id,
        "done": done,
        "name": self.name,
        "type": self.type,
        "flavor": self.flavor,
        "list_id": self.list_id
        }

    #Encontra item a partir do ID
    @classmethod
    def findById(cls,item_id):
        item = cls.query.filter_by(id = item_id).first()#Faz uma busca e retorna a primeira ocorrência
        if item:
            return item
        else:
            return None

    #Salva o item no banco
    def save(self):

        if not ListModel.findById(self.list_id):
            return { "message": "The associated list doesn't exists" }, 400

        database.session.add(self)
        database.session.commit()
        return { "message": "Item added successfully" }, 201


    #Atualiza o item no banco
    def update(self, name, type, flavor, list_id, done):
        print(name, type, flavor, list_id, done)
        self.name = name
        self.type = type
        self.flavor = flavor
        self.done = done
        ItemModel.save(self)

    #Deleta um item no banco
    def delete(self):
        database.session.delete(self)
        database.session.commit()
