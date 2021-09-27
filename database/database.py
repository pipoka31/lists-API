import sqlite3

connection = sqlite3.connect("Database.db")
cursor = connection.cursor()

# "\" serve para ele reconhecer que a proxima linha faz parte da string
createItemTable = "CREATE TABLE IF NOT EXISTS \
items (id integer PRIMARY KEY AUTOINCREMENT, name text, type text, flavor text, list_id integer, FOREIGN KEY(list_id) REFERENCES lists(id))"

createUserTable = "CREATE TABLE IF NOT EXISTS \
users (id integer PRIMARY KEY AUTOINCREMENT, name text, username text, password text)"

createListTable = "CREATE TABLE IF NOT EXISTS \
lists (id integer PRIMARY KEY AUTOINCREMENT, name text, status boolean, user_id integer, FOREIGN KEY(user_id) REFERENCES users(id))"


cursor.execute(createUserTable)#Cria a tabela
cursor.execute(createListTable)#Cria a tabela
cursor.execute(createItemTable)#Cria a tabela

connection.commit()
connection.close()
