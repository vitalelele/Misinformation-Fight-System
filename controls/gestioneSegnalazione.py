from flask import session
from models.segnalazione import Segnalazione
from models.notizia import Notizia
from models.notiziaTestuale import NotiziaTestuale
from models.immagine import Immagine
from models.audio import Audio
from models.video import Video
from dataAccessObject import DataAccessObject

class GestioneSegnalazione:
    def __init__(self,notizia : Notizia) -> None:
        self.__notizia = notizia

    def esisteSegnalazione(self):
        dbAccessObject = DataAccessObject()
        if isinstance(self.__notizia, NotiziaTestuale):
            segnalazioneDB = dbAccessObject.leggiDatabase("SELECT idSegnalazione FROM segnalazioni WHERE contenutoNotizia = %s AND urlNotizia = %s",(self.__notizia.getContenuto().lower(),self.__notizia.getUrl()))
            # Chiusura connessione
            if len(segnalazioneDB) == 1:
                # La segnalazione è presente nella tabella aggiorno il counter
                if session['isGiornalista'] == True:
                    dbAccessObject.scritturaDatabase("UPDATE segnalazioni SET counter = counter + 2 WHERE idSegnalazione = %s",(str(segnalazioneDB[0]['idSegnalazione'])))
                elif session['isUtente'] == True:
                    dbAccessObject.scritturaDatabase("UPDATE segnalazioni SET counter = counter + 1 WHERE idSegnalazione = %s",(str(segnalazioneDB[0]['idSegnalazione'])))
                return
            else:
                segnalazione = None
                if session['isUtente'] == True:
                    # La segnalazione non è presente nella tabella
                    segnalazione = Segnalazione(0,1,False,self.__notizia.getContenuto().lower(),self.__notizia.getUrl(),"testo")
                elif session['isGiornalista'] == True:

                    segnalazione = Segnalazione(0,2,False,self.__notizia.getContenuto().lower(),self.__notizia.getUrl(),"testo")
                segnalazione.inserisciDB()
        elif isinstance(self.__notizia, Immagine):
            segnalazioneDB = dbAccessObject.leggiDatabase("SELECT idSegnalazione FROM segnalazioni WHERE urlNotizia = %s",(self.__notizia.getUrl()))
            # Chiusura connessione
            if len(segnalazioneDB) == 1:
                #  La segnalazione è presente nella tabella aggiorno il counter
                if session['isGiornalista'] == True:
                    dbAccessObject.scritturaDatabase("UPDATE segnalazioni SET counter = counter + 2 WHERE idSegnalazione = %s",(str(segnalazioneDB[0]['idSegnalazione'])))
                elif session['isUtente'] == True:
                    dbAccessObject.scritturaDatabase("UPDATE segnalazioni SET counter = counter + 1 WHERE idSegnalazione = %s",(str(segnalazioneDB[0]['idSegnalazione'])))
                return
            else:
                segnalazione = None
                if session['isUtente'] == True:
                    # La segnalazione non è presente nella tabella
                    segnalazione = Segnalazione(0,1,False,"",self.__notizia.getUrl(),"immagine")
                elif session['isGiornalista'] == True:
                    segnalazione = Segnalazione(0,2,False,"",self.__notizia.getUrl(),"immagine")
                segnalazione.inserisciDB()
            
        elif isinstance(self.__notizia, Audio):
            segnalazioneDB = dbAccessObject.leggiDatabase("SELECT idSegnalazione FROM segnalazioni WHERE contenutoNotizia = %s",(self.__notizia.getContenuto().lower()))
            # Chiusura connessione
            if len(segnalazioneDB) == 1:
                # La segnalazione è presente nella tabella aggiorno il counter
                if session['isGiornalista'] == True:
                    dbAccessObject.scritturaDatabase("UPDATE segnalazioni SET counter = counter + 2 WHERE idSegnalazione = %s",(str(segnalazioneDB[0]['idSegnalazione'])))
                elif session['isUtente'] == True:
                    dbAccessObject.scritturaDatabase("UPDATE segnalazioni SET counter = counter + 1 WHERE idSegnalazione = %s",(str(segnalazioneDB[0]['idSegnalazione'])))
                return
            else:
                segnalazione = None
                if session['isUtente'] == True:
                    # La segnalazione non è presente nella tabella
                    segnalazione = Segnalazione(0,1,False,self.__notizia.getContenuto().lower(),"","audio")
                elif session['isGiornalista'] == True:
                    # Giusto per il meme non serve 
                    segnalazione = Segnalazione(0,2,False,self.__notizia.getContenuto().lower(),"","audio")
                segnalazione.inserisciDB()
        
        elif isinstance(self.__notizia, Video):
            segnalazioneDB = dbAccessObject.leggiDatabase("SELECT idSegnalazione FROM segnalazioni WHERE urlNotizia = %s",(self.__notizia.getUrl()))
            if len(segnalazioneDB) == 1:
                # La segnalazione è presente nella tabella aggiorno il counter
                if session['isGiornalista'] == True:
                    dbAccessObject.scritturaDatabase("UPDATE segnalazioni SET counter = counter + 2 WHERE idSegnalazione = %s",(str(segnalazioneDB[0]['idSegnalazione'])))
                elif session['isUtente'] == True:
                    dbAccessObject.scritturaDatabase("UPDATE segnalazioni SET counter = counter + 1 WHERE idSegnalazione = %s",(str(segnalazioneDB[0]['idSegnalazione'])))
                return
            else:
                segnalazione = None
                if session['isUtente'] == True:
                    # La segnalazione non è presente nella tabella
                    segnalazione = Segnalazione(0,1,False,"",self.__notizia.getUrl(),"video")
                elif session['isGiornalista'] == True:
                    # Giusto per il meme non serve 
                    segnalazione = Segnalazione(0,2,False,"",self.__notizia.getUrl(),"video")
                segnalazione.inserisciDB()
        return 