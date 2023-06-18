from models.giornalista import Giornalista, Utente
from models.amministratore import Amministratore
class GestioneAccesso:

    def accesso(self, utente: Utente, giornalista: Giornalista, amministratore: Amministratore):
        if utente is not None: 
            return utente.accedi()
        elif giornalista is not None:
            return giornalista.accedi()
        elif amministratore is not None:
            return amministratore.accedi()