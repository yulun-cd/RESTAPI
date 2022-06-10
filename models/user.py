import sqlite3


class UserModel():
    
    
    def __init__(self, userid, username, password):
        self.id = userid
        self.username = username
        self.password = password
    
        
    @classmethod    
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        
        if row: user = cls(*row)
        else: user = None
        
        connection.close()
        return user
    
    
    @classmethod    
    def find_by_id(cls, userid):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM users WHERE userid=?"
        result = cursor.execute(query, (userid,))
        row = result.fetchone()
        
        if row: user = cls(*row)
        else: user = None
        
        connection.close()
        return user