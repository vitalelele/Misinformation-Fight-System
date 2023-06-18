from models.amministratore import Amministratore
from models.giornalista import Giornalista
from models.segnalazione import Segnalazione
from dataAccessObject import DataAccessObject


class GestioneAmministratore:

    def giornalistiNonVerificati(self):
        dbAccessObject = DataAccessObject()
        giornalisti = dbAccessObject.leggiDatabase("SELECT * FROM giornalisti WHERE verificato=False",())
        return giornalisti
    
    def accettaGiornalista(self, giornalistaOk: Giornalista):
        # setto il verificato a True
        giornalistaOk.setVerificato(True)
        # print(giornalistaOk.getEmail(), flush=True)
        giornalistaOk.aggiornaVerificato()
        return True
    
    def rifiutaGiornalista(self, giornalistaNot: Giornalista):
        # setto il verificato a False
        # giornalistaNot.setVerificato(False)  #  <---- non serve poichè di default è settato a False
        
        # Aggiorno il DB, eliminando il giornalista dal db
        # eliminaDaDB() è un metodo di Giornalista
        giornalistaNot.eliminaDaDB()
        return True
    
    def restituisciSegnalazioni(self):
        dbAccessObject = DataAccessObject()
        segnalazioni = dbAccessObject.leggiDatabase("SELECT * FROM segnalazioni WHERE confermato=0",())
        for segnalazione in segnalazioni:
            segnalazione['contenutoNotizia'] = segnalazione['contenutoNotizia'].replace("\\'", "'")
        return segnalazioni
    
    def accettaSegnalazione(self, segnalazioneOk = Segnalazione):
        segnalazioneOk.setConfermato(True)
        segnalazioneOk.aggiornaConfermato()
        return True
    
    def rifiutaSegnalazione(self, segnalazioneNot = Segnalazione):
        segnalazioneNot.eliminaDaDB()
        return True