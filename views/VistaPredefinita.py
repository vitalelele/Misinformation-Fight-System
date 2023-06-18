from flask import render_template, request,session
from flask.views import View
from models.giornalista import Giornalista
from models.utente import Utente
from controls.gestioneRegistrazione import GestioneRegistrazione
from models.amministratore import Amministratore
from controls.gestioneRegistrazione import GestioneRegistrazione
from controls.gestioneAccesso import GestioneAccesso

# Classe che permette all’utente di utilizzare le funzionalità generali come registrazione e accesso
class vistaPredefinita(View):
    # Costruttore, il campo __sceltametodo serve per scegliere il metodo da eseguire
    def __init__(self,sceltaMetodo):
            self.__sceltametodo = sceltaMetodo
    
    # Metodo che viene chiamato dalla route nel file app, per esguire la richiesta 
    def dispatch_request(self):
        if self.__sceltametodo == 1:
            return self.Accesso()
        elif self.__sceltametodo == 2:
            return self.creazioneUtente()
        elif self.__sceltametodo == 3:
            return self.creazioneGiornalista()
    
    # Vista che gestisce l'accesso al sistema dell'utente o del giornalista
    def Accesso(self):
        # Variabile che contiene messaggio di errore
        msg = ''
        # Verifico che il metodo della richiesta sia POST e che i campi usernamee password del form siano stati compilati
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            # Creazione oggetti utente
            utente = Utente('','',request.form['username'],'',request.form['password'])
            # Creazione oggetto del controller della registrazione
            controlloAccesso = GestioneAccesso()
            # Verifico se l'utente può effettuare l'accesso al sistema, 
            # Verrà restituito true e un oggetto che contiene id e username se l'utente può effettuare l'acceso
            is_registrato, account = controlloAccesso.accesso(utente, None, None)
            print(type(account))
            print(account)
            if is_registrato:
                # Se l'accesso è andato a buon fine allora creo la sessione
                session['loggedin'] = True
                session['id'] = account[0]['id']
                session['username'] = account[0]['username']
                session['isUtente'] = True
                session['isGiornalista'] = False
                # Reindirizzamento alla pagina notizia.html
                return render_template('notizia.html')
            elif not is_registrato:
                # Se l'accesso non è andato a buon fine allora provo ad effettuare l'accesso da gionralista
                # Creazione oggetto giornalista
                giornalista = Giornalista('', '', request.form['username'],' ' ,request.form['password'],'','','')
                # Verifico se il giornalista può effettuare l'accesso al sistema, 
                is_registrato, account = controlloAccesso.accesso(None, giornalista, None)
                if is_registrato:
                    # Se l'accesso è andato a buon fine allora creo la sessione
                    session['loggedin'] = True
                    session['id'] = account[0]['id']
                    session['username'] = account[0]['username']
                    session['isUtente'] = False
                    session['isGiornalista'] = True
                     # Reindirizzamento alla pagina notizia.html
                    return render_template('notizia.html')
                elif not is_registrato:
                    amministratore = Amministratore('', '', request.form['username'], '', request.form['password'])
                    is_registrato, account = controlloAccesso.accesso(None, None, amministratore)        
                    if is_registrato:
                        session['loggedin'] = True
                        session['id'] = account[0]['id']
                        session['username'] = account[0]['username']
                        session['isGiornalista'] = False
                        session['admin'] = True
                        return render_template('amministratore.html', amministratore=amministratore)
                else:
                    msg = 'Username o password errati'
        # Reindirizzamento ala pagina login.html con messaggio di errore
        return render_template('login.html', msg=msg)
    
    # Vista che gestisce la registrazione al sistema dell'utente
    def creazioneUtente(self):
        # Variabile che contiene il messaggio di errore
        msg = ''
        # Verifico che il metodo della richiesta HTTP si POST e che tutti i campi del form sia stati compilati
        if request.method == 'POST' and 'nome' in request.form and 'cognome' in request.form and 'username' in request.form and 'email' in request.form and 'password' in request.form:
            # Creazione oggetto utente su cui saranno effettuati dei controlli
            utenteNonReg = Utente(request.form['nome'], request.form['cognome'],request.form['username'] ,request.form['email'],
                                         request.form['password'])
            # Creazione oggetto del controller della registrazione
            controlloUtente = GestioneRegistrazione()
            # Prova ad effettuare la registrazione, 
            # Se non è possibile effettuare la registrazione verra restituito un oggetto None e un messaggio di errore
            utente, msg = controlloUtente.registrazioneUtente(utenteNonReg)
            if utente is None:
                # Registrazione non possibile
                # Reindirizzamento alla pagina registrazioneUtente.html con messaggio di errore, e riempimento dei campi del form
                return render_template('registerUtente.html', msg=msg, nome=request.form['nome'],username=request.form['username'],
                                       cognome=request.form['cognome'],email=request.form['email'])
            else:
                # Registrazione effettuata
                # Reindirizzamento alla pagina di login con messaggio di conferma registrazione
                return render_template('login.html', msgregistrato='Registrazione effettuata, puoi effettuare il login')
        elif request.method == 'POST':
            # Il metodo della richiesta HTTP è POST però non sono stati compilati tutti i campi del form di registrazione
            # Reindirizzamento alla pagina registrazioneUtente.html
            msg = 'Perfavore completa il form'
            return render_template('registerUtente.html', msg=msg)
        # Il metodo della richiesta HTTP non è POST quindi verra mostrato il form di registrazione
        return render_template('registerUtente.html', msg=msg)
    
    # Vista che gestisce la registrazione al sistema del giornalista
    def creazioneGiornalista(self):
        # Variabile che contiene il messaggio di errore
        msg = ''
        # Verifico che il metodo della richiesta HTTP si POST e che tutti i campi del form sia stati compilati
        if request.method == 'POST' and 'nome' in request.form and 'cognome' in request.form and 'username' in request.form and 'email' in request.form and 'password' in request.form and 'matricola' in request.form and 'codiceFiscale' in request.form and 'regione' in request.form:
            # Creazione oggetto giornalisti su cui saranno effettuati dei controlli
            giornalistaNonReg = Giornalista(request.form['nome'], request.form['cognome'],request.form['username'] ,request.form['email'],
                                         request.form['password'], request.form['matricola'],
                                         request.form['codiceFiscale'], request.form['regione'])
            # Creazione oggetto del controller della registrazione
            controlloGiornalista = GestioneRegistrazione()
            # Prova ad effettuare la registrazione, 
            # Se non è possibile effettuare la registrazione verra restituito un oggetto None e un messaggio di errore
            giornalista, msg = controlloGiornalista.registrazioneGiornalista(giornalistaNonReg)
            if giornalista is None:
                # Registrazione non possibile
                # Reindirizzamento alla pagina registerGiornalista.html con messaggio di errore, e riempimento dei campi del form
                return render_template('registerGiornalista.html', msg=msg, nome=request.form['nome'],username=request.form['username'],
                                       cognome=request.form['cognome'],email=request.form['email'],
                                       matricola=request.form['matricola'],codiceFiscale=request.form['codiceFiscale'],regione=request.form['regione'])
            else:
                # Registrazione effettuata
                # Reindirizzamento alla pagina di login con messaggio di conferma registrazione
                return render_template('login.html', msgregistrato='Registrazione effettuata!')
        elif request.method == 'POST':
            # Il metodo della richiesta HTTP è POST però non sono stati compilati tutti i campi del form di registrazione
            # Reindirizzamento alla pagina registrazioneUtente.html, con messaggio di errore
            msg = 'Perfavore completa il form'
            return render_template('registerGiornalista.html', msg=msg)
        # Il metodo della richiesta HTTP non è POST quindi verra mostrato il form di registrazione
        return render_template('registerGiornalista.html', msg=msg)