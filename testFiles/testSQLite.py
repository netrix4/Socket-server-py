import sqlite3

SQLITE_DB = sqlite3.connect('SocketUsers.db')
DB_CURSOR = SQLITE_DB.cursor()

DB_CURSOR.execute("CREATE TABLE Users(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, username varchar(50) NOT NULL, password varchar(50))")
response = DB_CURSOR.execute("SELECT name FROM sqlite_master")
print(response.fetchall())

#Insert necesita commit() para efectuar
response = DB_CURSOR.execute('INSERT INTO Users (username, password) VALUES("Usuario Peru", "contrasena")')
SQLITE_DB.commit()
print(response.fetchall())

insertion_data = [('mario333', 'pass'),('Jhon Doe', 'passdoe')]
response = DB_CURSOR.executemany('INSERT INTO Users (username, password) VALUES(?, ?)', insertion_data)
SQLITE_DB.commit()

print(response.fetchall())

#Y select necesita fetch() para mostrar(bindear)
response = DB_CURSOR.execute('SELECT * FROM Users')

print(response.fetchall())

SQLITE_DB.close()