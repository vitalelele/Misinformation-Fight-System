from flask import render_template, request, session
from flask.views import View
from models.amministratore import Amministratore
from models.giornalista import Giornalista
from models.segnalazione import Segnalazione
from controls.gestioneAmministratore import GestioneAmministratore
from dataAccessObject import DataAccessObject

# io non ho ice perché ho già tutto il permafrost 
class vistaAmministratore(View):

    def dispatch_request(self):
        dbAccessObject = DataAccessObject()
        account = dbAccessObject.leggiDatabase("SELECT * FROM amministratori WHERE username = %s",(session['username']))
        if len(account) == 1:
            # Setto l'admin corrente
            currentAdmin = Amministratore(
                account[0]["nome"], account[0]["cognome"], account[0]["username"], account[0]["email"], account[0]["password"])
            # Istanzio il controller per l'amministratore
            controllerAdmin = GestioneAmministratore()

            try:
                if request.method == 'POST':
                    if session['loggedin'] and session['admin']:

                        # Button stampaGiornalisti
                        if request.form['submitButton'] == 'Stampa giornalisti':
                            giornalisti = self.stampaGiornalisti(controllerAdmin)
                            if not giornalisti:
                                return render_template('amministratore.html', msgNoGiornalisti=True)
                            else:
                                return render_template('amministratore.html', allGiornalisti=giornalisti)

                        # Se ha premuto il tasto per accettare una richiesta
                        elif request.form['submitButton'] == 'Accetta':
                            giornalista = self.accettaGiornalista(controllerAdmin)
                            # Mi serve poiché comunque voglio rimostrare la lista dei giornalisti non verificati
                            giornalisti = self.stampaGiornalisti(controllerAdmin)
                            return render_template('amministratore.html', allGiornalisti=giornalisti, msgOk="accettato", nomeGiornalista=giornalista.getNome())

                        # Button rifiuta
                        elif request.form['submitButton'] == 'Rifiuta':
                            giornalista = self.rifiutaGiornalista(controllerAdmin)
                            # Se rifiuto devo fare una query che elimina il giornalista dal database ?
                            giornalisti = self.stampaGiornalisti(controllerAdmin)
                            return render_template('amministratore.html', allGiornalisti=giornalisti, msgOk="rifiutato", nomeGiornalista=giornalista.getNome())

                        elif request.form['submitButton'] == 'Chiudi lista':
                            return render_template('amministratore.html')
                        
                        elif request.form['submitButton'] == 'Stampa segnalazioni':
                            segnalazioni = self.stampaSegnalazioni(controllerAdmin)
                            if not segnalazioni:
                                return render_template('amministratore.html', msgNoSegnalazioni=True)
                            else:
                                return render_template('amministratore.html', allSegnalazioni=segnalazioni)
                        
                        elif request.form['submitButton'] == 'Accetta Segnalazione':
                            self.accettaSegnalazione(controllerAdmin)
                            segnalazioni = self.stampaSegnalazioni(controllerAdmin)
                            return render_template('amministratore.html', allSegnalazioni=segnalazioni, msgOkSegn='accettata')
                        
                        elif request.form['submitButton'] == 'Rifiuta Segnalazione':
                            self.rifiutaSegnalazione(controllerAdmin)
                            segnalazioni = self.stampaSegnalazioni(controllerAdmin)
                            return render_template('amministratore.html', allSegnalazioni=segnalazioni, msgOkSegn='rifiutato')
                    else:
                        return render_template('notLoggedIn.html')
                    
            except KeyError:
                return render_template('404Error.html')
        
    def stampaSegnalazioni(self, controllerAdmin: GestioneAmministratore):
        segnalazioni = controllerAdmin.restituisciSegnalazioni()
        return segnalazioni


    def stampaGiornalisti(self, controllerAdmin: GestioneAmministratore):
        giornalisti = controllerAdmin.giornalistiNonVerificati()
        return giornalisti

    def accettaGiornalista(self, controllerAdmin: GestioneAmministratore):
        # Se lo accetto allora bisogna fare una query che modifica lo stato verificato del giornalista
        idGiornalistaOk = request.form['idGiornalista']
        dbAccessObject  = DataAccessObject()
        resultQuery = dbAccessObject.leggiDatabase("SELECT * FROM giornalisti WHERE id = %s ", (idGiornalistaOk))
        # Creo il giornalista
        giornalistaOk = Giornalista(resultQuery[0]['nome'], resultQuery[0]['cognome'], resultQuery[0]['username'], resultQuery[0]['email'],
                                    resultQuery[0]['password'], resultQuery[0]['matricola'], resultQuery[0]['codiceFiscale'], resultQuery[0]['regione'])
        # Il controller accetta il giornalista e ne modifica l'attributo verificato settandolo a True
        controllerAdmin.accettaGiornalista(giornalistaOk)
        return giornalistaOk

    def rifiutaGiornalista(self, controllerAdmin: GestioneAmministratore):
        idGiornalistaNot = request.form['idGiornalista']
        dbAccessObject  = DataAccessObject()
        resultQuery = dbAccessObject.leggiDatabase("SELECT * FROM giornalisti WHERE id = %s ", (idGiornalistaNot))
        # Creo il giornalista
        giornalistaNot = Giornalista(resultQuery[0]['nome'], resultQuery[0]['cognome'], resultQuery[0]['username'], resultQuery[0]['email'],
                                     resultQuery[0]['password'], resultQuery[0]['matricola'], resultQuery[0]['codiceFiscale'], resultQuery[0]['regione'])
        # Il controller accetta il giornalista e ne modifica l'attributo verificato settandolo a True
        controllerAdmin.rifiutaGiornalista(giornalistaNot)
        return giornalistaNot

    def accettaSegnalazione(self, controllerAdmin: GestioneAmministratore):
        idSegnalazione = request.form['idSegnalazione']
        dbAccessObject = DataAccessObject()
        resultQuery = dbAccessObject.leggiDatabase("SELECT * FROM segnalazioni WHERE idSegnalazione = %s ", (idSegnalazione))
        segnalazioneOk = Segnalazione(resultQuery[0]['idSegnalazione'], resultQuery[0]['counter'], resultQuery[0]['confermato'], resultQuery[0]['contenutoNotizia'], resultQuery[0]['urlNotizia'], "")
        controllerAdmin.accettaSegnalazione(segnalazioneOk)
        return segnalazioneOk

    def rifiutaSegnalazione(self, controllerAdmin = GestioneAmministratore):
        idSegnalazione = request.form['idSegnalazione']
        dbAccessObject = DataAccessObject()
        resultQuery = dbAccessObject.leggiDatabase("SELECT * FROM segnalazioni WHERE idSegnalazione = %s", (idSegnalazione))
        segnalazioneNot = Segnalazione(resultQuery[0]['idSegnalazione'], resultQuery[0]['counter'], resultQuery[0]['confermato'], resultQuery[0]['contenutoNotizia'], resultQuery[0]['urlNotizia'],"")
        controllerAdmin.rifiutaSegnalazione(segnalazioneNot=segnalazioneNot)
        return segnalazioneNot