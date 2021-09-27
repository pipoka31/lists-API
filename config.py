#Mudar no app.py
#app.config["SQALCHEMY_DATABASE_URI"] = "postgres://user:password@localhost:port/databaseName"

#import psycopg2

##no lugar de connection = sqlite3.connect("Database.db") =>
#psycopg2.connect(
# user = "username",
# password = "password",
# host = "localhost",
# port = 3000,
# database = "databaseName"
# )

#Ao executar um comando com a variavel cursor, ela nao retorna nada, apenas retorna =>
#result = cursor.fetchall()
