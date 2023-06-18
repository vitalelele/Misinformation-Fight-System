from dataAccessObject import DataAccessObject
import hashlib


class Amministratore():
    def __init__(self, nome, cognome, username, email, password):
        self.__nome = nome
        self.__cognome = cognome
        self.__username = username
        self.__email = email
        self.__password = hashlib.sha256(password.encode()).hexdigest()
    
    def getNome(self):
        return self.__nome
    
    def setNome(self, nome):
        self.__nome = nome

    def getCognome(self):
        return self.__cognome
    
    def setCognome(self, cognome):
        self.__cognome = cognome

    def getUsername(self):
        return self.__username
    
    def setUsername(self, username): 
        self.__username = username

    def getEmail(self):
        return self.__email
    
    def setEmail(self, email):
        self.__email = email

    def getPassword(self):
        return self.__password

    def accedi(self):
        dbAccessObject = DataAccessObject()
        account = dbAccessObject.leggiDatabase("SELECT * FROM amministratori WHERE username = %s AND password = %s",(self.getUsername(), self.getPassword()))
        if len(account) == 1:
            return True, account
        return False, None
