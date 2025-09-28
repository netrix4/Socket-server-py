import sqlite3
from DTOs.UserAuthResponse import UserAuthResponse

class SQLiteProvider:
    _SQLITE_DB = None
    _DB_CURSOR = None
    
    def __init__(self, db_name):
        self._SQLITE_DB = sqlite3.connect(db_name)
        self._DB_CURSOR = self._SQLITE_DB.cursor()

    def isValidUser(self, user: tuple):
        response = self._DB_CURSOR.execute('SELECT * FROM Users WHERE username = ? AND password = ?', user).fetchone()
        
        if response is None:
            userResponse = UserAuthResponse(status=500, message="User not found", user_id=0)
        else:
            userResponse = UserAuthResponse(status=200, message="Ok", user_id=response[0])

        self._SQLITE_DB.close()
        return userResponse
    
    def insertNewUser(self, user: tuple):
        response = self._DB_CURSOR.execute('INSERT INTO Users (username, password) VALUES (?,?)', user).fetchone()
        self._SQLITE_DB.close()
        return response
    
    def getUserDataByUsername(self, username: str ):
        response = self._DB_CURSOR.execute(f'SELECT * FROM Users WHERE username = "{username}"').fetchone()
        
        if response is None:
            userResponse = UserAuthResponse(status=500, message="User not found", user_id=0)
        else:
            userResponse = UserAuthResponse(status=200, message="Ok", user_id=response[0])

        self._SQLITE_DB.close()
        return userResponse