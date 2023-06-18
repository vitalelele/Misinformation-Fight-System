from models.giornalista import Giornalista, Utente
from models.amministratore import Amministratore
import re

# Controller che riceve i dati inseriti dall’utente o dal giornalista tramite la vista, li elabora, 
# Eventualmente accedendo ai servizi esportati dal model, così da permettere la registrazione al sistema.
class GestioneRegistrazione:

    # Funzione che effettua la registrazione del giornalista nel sistema
    # Se la registrazione viene effettuata con successo restituisce un oggetto giornalista e un messaggio vuoto
    # Altrimenti restituisce un oggetto nullo e un messaggio di errore
    def registrazioneGiornalista(self, giornalistaTemp: Giornalista):
        # Variabile che contiene il messaggio di errore nel caso di registrazione non riuscita
        msg=''
        # Verifica che il giornalista non sia presente nel database
        if giornalistaTemp.is_in_DB():
            msg = 'Account già esistente!'
            return None, msg
        # Verifico che i dati inseriti per la registrazione siano corretti
        controllo, msg = self.controllaDati(giornalistaTemp)
        if controllo == True:
            if giornalistaTemp.memorizzaDB(): # Memorizzo il giornalista nel database
                msg = 'Ti sei registrato correttamente'
                return giornalistaTemp, msg
        return None, msg

    # Metodo che effetua la registrazione dell'utente nel sistema
    # Se la registrazione viene effettuata con successo restituisce un oggetto utente e un messaggio vuoto
    # Altrimenti restituisce un oggetto nullo e un messaggio di errore
    def registrazioneUtente(self, utenteTemp: Utente):
        # Variabile che contiene il messaggio di errore nel caso di registrazione non riuscita
        msg = ''
        # Verifica che l'utente non sia presente nel database
        if utenteTemp.is_in_DB():
            msg = 'Account già esistente!'
            return None, msg
        # Verifica che l'email del giornalista abbia un formato corretto
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', utenteTemp.getEmail()):
            msg = 'Indirizzo email non valido'
            return None,msg
        else:
            # Memorizza l'utente nel database
            if utenteTemp.memorizzaDB():
                msg = 'Ti sei registrato correttamente'
                return utenteTemp, msg
        return None, msg

    # Metodo che esegue l'accesso (dell'utente o del giornalista)al sistema
    # Verrà eseguito l'accesso dell'oggetto che non ha un valore None
    def accesso(self, utente: Utente, giornalista: Giornalista, amministratore: Amministratore):
        if utente is not None: 
            return utente.accedi()
        elif giornalista is not None:
            return giornalista.accedi()
        elif amministratore is not None:
            return amministratore.accedi()

    # Verfica se i l'email, la matricola e il codice Fiscae del giornalista sono corretti 
    # Tramite delle regex viene verficato se questi dati rispettano il loro formato
    def controllaDati(self,g: Giornalista):
        # Variabile che contiene un messaggio di errore nel caso di dati sbagliati
        msg = ''
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', g.getEmail()):
            msg = 'Indirizzo email non valido'
            return False,msg
        elif not re.match(r'^\d{6}[a-zA-Z]$',g.getMatricola()):
            msg = 'Matricola non valida'
            return False, msg
        elif not re.match(r'^[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]$',g.getCodiceFiscale()):
            msg = 'Codice fiscale non valido'
            return False, msg
        elif not g.getPassword() or not g.getEmail() or not g.getNome() or not g.getCodiceFiscale() or not g.getMatricola() or not g.getRegione() or not g.getCogonme():
            msg = 'Perfavore, compila tutto il form'
            return False, msg
        return True, msg