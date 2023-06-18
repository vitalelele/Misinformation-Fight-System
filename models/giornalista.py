from .utente import Utente
from dataAccessObject import DataAccessObject

# Classe che modella il giornalista
class Giornalista(Utente):
    # Costruttore
    def __init__(self, nome, cognome, username, email, password, matricola, codiceFiscale, regione):
        super().__init__(nome, cognome, username, email, password)
        self.__matricola = matricola
        self.__codiceFiscale = codiceFiscale
        self.__regione = regione
        self.__verificato = False

    def setMatricola(self, matricola):
        self.__matricola = matricola

    def getMatricola(self):
        return self.__matricola

    def setCodiceFiscale(self, codiceFiscale):
        self.__codiceFiscale = codiceFiscale

    def getCodiceFiscale(self):
        return self.__codiceFiscale

    def setRegione(self, regione):
        self.__regione = regione

    def getRegione(self):
        return self.__regione

    def setVerificato(self, valore: bool):
        self.__verificato = valore

    def getVerificato(self):
        return self.__verificato

    # Verifica se l'userneme e la password del giornalista sono presenti nel database
    # Ritorna True, id del giornalsta e username solo se entrambi sono presenti nel database
    def accedi(self):
        dbAccessObject = DataAccessObject()
        account = dbAccessObject.leggiDatabase("SELECT id,username FROM giornalisti WHERE username = %s AND password = %s AND verificato = true",
                                               (super().getUsername(),super().getPassword()))
        if len(account) == 1:
            return True, account
        return False, None

    # Verifica se l'username e l'username del giornalista sono presenti nel database
    def is_in_DB(self):
        dbAccessObject = DataAccessObject()
        account = dbAccessObject.leggiDatabase("SELECT email,username FROM giornalisti WHERE email = %s or username = %s",
                                               (super().getEmail(),super().getUsername()))
        if account:
            return True
        return False

    # Inserimento del giornalista nel database
    def memorizzaDB(self):
        dbAccessObject = DataAccessObject()
        if dbAccessObject.scritturaDatabase("INSERT INTO giornalisti VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, false)",(super().getNome(),super().getCogonme(),
                                                                                                                            super().getUsername(),super().getEmail(),
                                                                                                                            super().getPassword(),self.__matricola,
                                                                                                                            self.__codiceFiscale,self.__regione)):
            return True
        return False

    # Aggiunto per aggiornare il DB
    def aggiornaVerificato(self):
        dbAccessObject = DataAccessObject()
        if dbAccessObject.scritturaDatabase("UPDATE giornalisti SET verificato=%s WHERE matricola = %s",(self.getVerificato(),self.getMatricola())):
            return True
        return False

    # Aggiunto per eliminare il giornalista dal database
    def eliminaDaDB(self):
        dbAccessObject = DataAccessObject()
        if dbAccessObject.scritturaDatabase("DELETE FROM giornalisti WHERE matricola = %s",(self.getMatricola())):
            return True
        return False
