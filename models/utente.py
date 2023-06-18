from dataAccessObject import DataAccessObject
import hashlib
# Per hashare in sha256() con hashlib.sha256(b'Passare in byte!')

# Classe che modella l’utente, è generalizzazione della sottoclasse Giornalista
class Utente:
    # Costruttore
    def __init__(self,nome,cognome,username,email,password):
        self.__nome = nome
        self.__cognome = cognome
        self.__username = username
        self.__email = email
        # Hexdigest serve per salvare l'hash come stringa
        self.__password = hashlib.sha256(password.encode()).hexdigest()

    def setNome(self,nome):
        self.__nome = nome
    def getNome(self):
        return self.__nome

    def setCognome(self,cognome):
        self.__cognome = cognome
    def getCogonme(self):
        return self.__cognome

    def setUsername(self, username):
        self.__username = username
    def getUsername(self):
        return self.__username

    def setEamil(self,email):
        self.__email = email
    def getEmail(self):
        return self.__email

    def setPassword(self,password):
        self.__password = password
    def getPassword(self):
        return self.__password

    def setIdUtente(self,idUtente):
        self.__idUtente = idUtente

    def getIdUtente(self):
        return self.__idUtente

    # Verifica se l'userneme e la password dell'utente sono presenti nel database
    # Ritorna True,id dell'utente e username solo se entrambi sono presenti nel database
    def accedi(self):
        dbAccessObject = DataAccessObject()
        account = dbAccessObject.leggiDatabase("SELECT id,username FROM utenti WHERE username = %s AND password = %s",
                                               (self.__username,self.__password))
        if len(account) == 1:
            return True, account
        else:
            # Se l'utente non è presente nella tabella degli utenti normali verifico se è presente nei giornalisti non verificati (che sono considerati come utenti normali)
            dbAccessObject = DataAccessObject()
            account = dbAccessObject.leggiDatabase("SELECT id,username FROM giornalisti WHERE username = %s AND password = %s AND verificato = false",
                                               (self.__username,self.__password))
            if len(account) == 1:
                return True, account
        return False, None

    # Verifica se l'username o la password dell'utente sono presenti nel database
    def is_in_DB(self):
        dbAccessObject = DataAccessObject()
        account = dbAccessObject.leggiDatabase("SELECT email,username FROM utenti WHERE email = %s OR username = %s",
                                               (self.__email,self.__username))
        if account:
            return True
        return False
    
    # Memorizza l'utente nel database
    def memorizzaDB(self):
        dbAccessObject = DataAccessObject()
        if dbAccessObject.scritturaDatabase("INSERT INTO utenti VALUES (NULL, %s, %s, %s,%s, %s)",(self.__nome,self.__cognome,
                                                                                                   self.__username,self.__email,self.__password)):
            return True
        return False


