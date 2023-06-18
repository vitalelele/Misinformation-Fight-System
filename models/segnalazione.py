from dataAccessObject import DataAccessObject

class Segnalazione:
    def __init__(self,idSegnalazione,counter,confermato,contenuto,url,tipo):
        self.__idSegnalazione = idSegnalazione
        self.__counter = counter
        self.__confermato = confermato
        self.__contenutoNotizia = contenuto
        self.__urlNotizia = url
        self.__tipo = tipo
    

    def getIdSegnalazione(self):
        return self.__idSegnalazione
    
    def getCounter(self):
        return self.__counter

    def setCounter(self,counter):
        self.__counter = counter

    def getConfermato(self):
        return self.__confermato

    def setConfermato(self,confermato):
        self.__confermato = confermato

    def getContenutoNotizia(self):
        return self.__contenutoNotizia

    def setContenutoNotizia(self,contenuto):
        self.__contenutoNotizia = contenuto
    
    def getUrlNotizia(self):
        return self.__urlNotizia

    def setUrlNotizia(self,url):
        self.__urlNotizia = url

    def getTipo(self):
        return self.__tipo

    def setTipo(self,tipo):
        self.__tipo = tipo
    
    def eliminaDaDB(self):
        dbAccessObject = DataAccessObject()
        dbAccessObject.scritturaDatabase("DELETE FROM segnalazioni WHERE idSegnalazione = %s", (str(self.__idSegnalazione)))
        return True
    
    def aggiornaConfermato(self):
        dbAccessObject = DataAccessObject()
        dbAccessObject.scritturaDatabase("UPDATE segnalazioni SET confermato=%s WHERE idSegnalazione = %s", (self.__confermato,self.__idSegnalazione))
        return True

    def inserisciDB(self):
        dbAccessObject = DataAccessObject()
        dbAccessObject.scritturaDatabase("INSERT INTO segnalazioni (counter,contenutoNotizia,urlNotizia,tipo) VALUES (%s,%s, %s, %s)",(self.__counter,self.__contenutoNotizia,self.__urlNotizia,self.__tipo))