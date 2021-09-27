from sql_alchemy import database

class UserModel(database.Model):

    #Tabela ao qual esse modelo pertence
    __tablename__ = "users"

    #Define o tipo de campo que sera adicionado ao BD
    id = database.Column(database.Integer(), primary_key = True)
    name = database.Column(database.String(100))
    username = database.Column(database.String(100))
    password = database.Column(database.String(100))
    lists = database.relationship("ListModel") #Lista de "lists"

    def __init__(self,id,name,username,password):
        self.name = name
        self.username = username
        self.password = password


    def json(self):
        return {
        "id": self.id,
        "name": self.name,
        "username": self.username,
        "lists": [ list.json() for list in self.lists ]
        }

    #Encontra item a partir do ID
    @classmethod
    def findById(cls,user_id):
        user = cls.query.filter_by(id = user_id).first()#Faz uma busca e retorna a primeira ocorrência
        if user:
            return user
        else:
            return None

    @classmethod
    def findByUsername(cls,username):
        user = cls.query.filter_by(username = username).first()
        if user:
            return user
        else:
            return None

    #Salva o item no banco
    def save(self):
        database.session.add(self)
        database.session.commit()

    #Atualiza o item no banco
    def update(self,id,name,username,password):
        self.name = name
        self.username = username
        self.password = password
        UserModel.save(self)

    #Deleta um item no banco
    def delete(self):
        database.session.delete(self)
        database.session.commit()
