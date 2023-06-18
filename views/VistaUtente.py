from flask import render_template, request, session, current_app
from flask.views import View
from models.notiziaTestuale import NotiziaTestuale
from models.immagine import Immagine
from models.notizia import Notizia
from models.audio import Audio
from models.video import Video
from controls.gestioneNotizieAnaloghe import GestioneNotizieAnaloghe
from controls.gestioneIndiceAttendibilita import GestioneIndiceAttendibilita
from controls.gestioneFontiAttendibili import GestioneFontiAttendibili
from controls.gestioneSegnalazione import GestioneSegnalazione
import pathlib
import speech_recognition as sr
from pydub import AudioSegment
import validators # Per verificare se è un URL il plain text
import requests
import urllib
import sys
from pathlib import Path
import argparse
import urllib.request
from pytube import YouTube

# Classe che permette all’utente di interagire con il sistema utilizzando le funzionalità a lui offerte e di visualizzare i dati


class vistaUtente(View):
    # Costruttore, il campo __sceltametodo serve per scegliere il metodo da eseguire
    def __init__(self, selezionametodo):
        self.__selezionametodo = selezionametodo

    # Metodo che viene chiamato dalla route nel file app, per esguire la richiesta
    def dispatch_request(self):
        if self.__selezionametodo == 1:
            return self.InserimentoNotizia()
        if self.__selezionametodo == 2:
            return self.InserimentoNotiziaTesto()
        if self.__selezionametodo == 3:
            return self.InserimentoNotiziaImmagine()
        if self.__selezionametodo == 4:
            return self.InserimentoNotiziaAudio()
        if self.__selezionametodo == 5:
            return self.InserimentoNotiziaVideo()
        if self.__selezionametodo == 6:
            return self.segnalaNotizia()
        

    def VerificaAttendibilita(notizia: Notizia):
        # Controllo se la notizia è testuale
        if isinstance(notizia, NotiziaTestuale):

            # Calcolo l'indice
            indice_attendibilita = GestioneIndiceAttendibilita()

            criteri = indice_attendibilita.calcoloIndiceTesto(notizia)
            notizia.setIndiceAttendibilita(criteri[0])

            # Notizie simili
            contrNotizieAnaloghe = GestioneNotizieAnaloghe(notizia)
            # Creazione di una lista che conterrà le notizie analoghe individuate tramite il metodo notizieAnaloghe() del controller
            notizieAnaloghe = contrNotizieAnaloghe.notizieAnalogheTesto()

            #  #  Per calcolare l'indice di attendibilità su ogni notizia analoga
            #  # Se li calcolo tutti -> tempi di esecuzione troppo lunghi!
            # X = 70
            # notizieAnalogheAttendibili = []
            # # per ogni notizia in notizieAnaloghe calcolo l'indice
            # for notizia in notizieAnaloghe:
            #     if indice_attendibilita.calcoloIndiceTesto(notizia)[0] > X:
            #         notizieAnalogheAttendibili.append(notizia)

            # Passo questo url perchè se usiamo l'api di google, ci stamperà questo url per primo, qundi in notiziaTesto.html verifico che non sia questo
            is_valid_url = "https://support.google.com/websearch/answer/106230?hl=it"

            #   return render_template('notiziaTesto.html', notizieAnaloghe=notizieAnalogheAttendibili, criteri=criteri, is_valid_url=is_valid_url)
            if notizieAnaloghe:
                return render_template('notiziaTesto.html', notiziaInserita=notizia, notizieAnaloghe=notizieAnaloghe, criteri=criteri, is_valid_url=is_valid_url)
            else:
                msgNotNotizie = "Non sono state trovate notizie analoghe."
                return render_template('notiziaTesto.html',notiziaInserita=notizia, msgNotNotizie=msgNotNotizie, notizieAnaloghe=notizieAnaloghe, criteri=criteri, is_valid_url=is_valid_url)


        # Controllo se la notizia è un'immagine
        if isinstance(notizia, Immagine):

             # Calcolo l'indice
            indice_attendibilita = GestioneIndiceAttendibilita()
            criteri = indice_attendibilita.calcoloIndiceImmagine(notizia)
            notizia.setIndiceAttendibilita(criteri[0])

            # Notizie analoghe
            contrNotizieAnaloghe = GestioneNotizieAnaloghe(notizia)
            # Creazione di una lista che conterrà le notizie analoghe individuate tramite il metodo notizieAnaloghe() del controller
            notizieAnaloghe = contrNotizieAnaloghe.notizieAnalogheImmagine()
            
            if notizieAnaloghe:
                return render_template('notiziaImmagine.html', notiziaInserita=notizia, notizieAnaloghe=notizieAnaloghe, criteri=criteri)
            else:
                msgNotNotizie = "Non sono state trovate notizie analoghe."
                return render_template('notiziaImmagine.html',notiziaInserita=notizia, msgNotNotizie=msgNotNotizie, notizieAnaloghe=notizieAnaloghe, criteri=criteri)

        # Controllo se la notizia è un audio
        if isinstance(notizia, Audio):
            # Calcolo l'indice
            indice_attendibilita = GestioneIndiceAttendibilita()

            criteri = indice_attendibilita.calcoloIndiceAudio(notizia)
            notizia.setIndiceAttendibilita(criteri[0])

            # Notizie analoghe
            contrNotizieAnaloghe = GestioneNotizieAnaloghe(notizia)
            # Creazione di una lista che conterrà le notizie analoghe individuate tramite il metodo notizieAnaloghe() del controller
            notizieAnaloghe = contrNotizieAnaloghe.notizieAnalogheAudio()

            #  #  Per calcolare l'indice di attendibilità su ogni notizia analoga
            #  # Se li calcolo tutti -> tempi di esecuzione troppo lunghi!
            # X = 70
            # notizieAnalogheAttendibili = []
            # # per ogni notizia in notizieAnaloghe calcolo l'indice
            # for notizia in notizieAnaloghe:
            #     if indice_attendibilita.calcoloIndiceTesto(notizia)[0] > X:
            #         notizieAnalogheAttendibili.append(notizia)

            # passo questo url perchè se usiamo l'api di google, ci stamperà questo url per primo, qundi in notiziaTesto.html verifico che non sia questo
            is_valid_url = "https://support.google.com/websearch/answer/106230?hl=it"

            #   return render_template('notiziaTesto.html', notizieAnaloghe=notizieAnalogheAttendibili, criteri=criteri, is_valid_url=is_valid_url)
            if notizieAnaloghe:
                return render_template('notiziaAudio.html', notiziaInserita=notizia, notizieAnaloghe=notizieAnaloghe, criteri=criteri, is_valid_url=is_valid_url)
            else:
                msgNotNotizie = "Non sono state trovate notizie analoghe."
                return render_template('notiziaAudio.html',notiziaInserita=notizia, msgNotNotizie=msgNotNotizie, notizieAnaloghe=notizieAnaloghe, criteri=criteri, is_valid_url=is_valid_url)

        # Controllo se la notizia è un'immagine
        if isinstance(notizia, Video):

             # Calcolo l'indice
            indice_attendibilita = GestioneIndiceAttendibilita()
            criteri = indice_attendibilita.calcoloIndiceVideo(notizia)
            notizia.setIndiceAttendibilita(criteri[0])

            # Notizie simili
            contrNotizieAnaloghe = GestioneNotizieAnaloghe(notizia)
            # Creazione di una lista che conterrà le notizie analoghe individuate tramite il metodo notizieAnaloghe() del controller
            notizieAnaloghe = [0]
            
            for path in Path("temp/Video/frame").iterdir():
                if path.is_file():
                    path.unlink()
            for path in Path("temp/Video").iterdir():
                if path.is_file():
                    path.unlink()
                    
            if notizieAnaloghe:
                return render_template('notiziaVideo.html', notiziaInserita=notizia, notizieAnaloghe=notizieAnaloghe, criteri=criteri)
            else:
                msgNotNotizie = "Non sono state trovate notizie analoghe."
                return render_template('notiziaVideo.html',notiziaInserita=notizia, msgNotNotizie=msgNotNotizie, notizieAnaloghe=notizieAnaloghe, criteri=criteri)




    def individuaFontiAttendibili(notizia: Notizia):

        # Controllo se la notizia è testuale   
        if isinstance(notizia, NotiziaTestuale):
            
            fonti = GestioneFontiAttendibili(notizia)
            fontiAttendibili = fonti.fontiAttendibili()
            # Mostro fonti attendibili
            return render_template('notiziaTesto.html', fontiAttendibili=fontiAttendibili)
        
        # controllo se la notizia un immagine   
        if isinstance(notizia, Immagine):
            
            fonti = GestioneFontiAttendibili(notizia)
            fontiAttendibili = fonti.fontiAttendibili()
            # mostro fonti attendibili
            return render_template('notiziaImmagine.html', fontiAttendibili=fontiAttendibili)
        
        # Controllo se la notizia è un audio   
        if isinstance(notizia, Audio):
            
            fonti = GestioneFontiAttendibili(notizia)
            fontiAttendibili = fonti.fontiAttendibili()
            # Mostro fonti attendibili
            return render_template('notiziaAudio.html', fontiAttendibili=fontiAttendibili)
        
        if isinstance(notizia, Video):
            
            fontiAttendibili = [0]
            # Mostro fonti attendibili
            return render_template('notiziaVideo.html', fontiAttendibili=fontiAttendibili)


    # Metodo che permette all'utente di inserire una notizia testuale che potra essere utilizzata successivamente
    def InserimentoNotizia(self):
        try:
            # Controllo se l'utente è loggato
            if session['loggedin']:
                return render_template('notizia.html')
            else:
                # Se non lo è allora redirect alla pagina di login
                return render_template('login.html')
            # return redirect(url_for('login'), msgQuit="You're not logged in.")
        except KeyError:
            return render_template('notLoggedIn.html')

    def InserimentoNotiziaTesto(self):
        try:
            # Controllo se l'utente è loggato
            if 'loggedin' in session and session['loggedin']:
                plainText = None

                # Verifico che il metodo della richiesta HTTP sia POST
                if request.method == 'POST':
                    # Recupero il contenuto della textArea dell form cioè la notizia inserita dall'utente
                    plainText = request.form['inputTesto']
                    # Controllo che l'unente ha inserito qualcosa, se non lo ha fatto stampo messaggio di errore
                    if plainText == '':
                        errore = 'si prega di inserire un testo o un url'
                        return render_template('notiziaTesto.html', errore=errore)

                    else:

                        # Controllo se la notizia è un URL o un testo
                        if validators.url(plainText) is True:
                            # Estraiamo il testo contenuto nell'URL
                            tokenApi = "4ac42c52447f1cc24cfce1f02b2ae6db"
                            queryEncoded = urllib.parse.quote(
                                plainText, safe='')
                            url = f"https://api.diffbot.com/v3/analyze?url={queryEncoded}&token={tokenApi}"
                            headers = {"accept": "application/json"}
                            response = requests.get(url, headers=headers)
                            data = response.json()
                            self.miaNotiziaTestuale = NotiziaTestuale(
                                0, '', '', plainText, data['objects'][0]['title'])
                        else:
                            self.miaNotiziaTestuale = NotiziaTestuale(
                                0, '', plainText, None, plainText)

                        # Verifico che l'utente ha richiesto di calcolare l'indice della notizia testuale
                        if request.form.get('calcolaIndice') is not None:
                            return vistaUtente.VerificaAttendibilita(self.miaNotiziaTestuale)
                        # Verifico che l'utente ha richiesto di mostrate fonti attendibili
                        if request.form.get('fontiAttendibili') is not None:
                            return vistaUtente.individuaFontiAttendibili(self.miaNotiziaTestuale)
                else:
                    # Reindirizzo alla pagina
                    return render_template('notiziaTesto.html')

            else:
                # Se non lo è allora redirect alla pagina di login
                return render_template('login.html', flag=True)
            # return redirect(url_for('login'), msgQuit="You're not  logged in.")
        except KeyError:
            return render_template('notLoggedIn.html')



    def InserimentoNotiziaImmagine(self):
        try:
            # Controllo se l'utente è loggato
            if 'loggedin' in session and session['loggedin']:
                plainImm = None

                # Verifico che il metodo della richiesta HTTP si POSt
                if request.method == 'POST':
                    # Recupero il contenuto della textArea dell form cioè la notizia inserita dall'utente
                    plainImm = request.form['inputImmagine']
                    # Controllo che l'unente ha inserito qualcosa, se non lo ha fatto stampo messaggio di errore
                    if plainImm == '':
                        errore = 'si prega di inserire un url'
                        return render_template('notiziaImmagine.html', errore=errore)

                    else:

                        # Controllo se l'utente ha inserito un URL
                        if validators.url(plainImm) is True:
                            self.miaNotiziaImmagine = Immagine(0, '', '', plainImm, '', '', '')
                        else:
                            errore = 'si prega di inserire un url'
                            return render_template('notiziaImmagine.html', errore=errore)

                        # Verifico che l'utente ha richiesto di calcolare l'indice dell'immagine
                        if request.form.get('calcolaIndice') is not None:
                            return vistaUtente.VerificaAttendibilita(self.miaNotiziaImmagine)
                        
                        # Verifico che l'utente ha richiesto di mostrate fonti attendibili
                        if request.form.get('fontiAttendibili') is not None:
                            # Verifico che l'utente ha richiesto di mostrate fonti attendibili
                            return vistaUtente.individuaFontiAttendibili(self.miaNotiziaImmagine)
                        
                else:
                    # Reindirizzo alla pagina
                    return render_template('notiziaImmagine.html')

            else:
                # Se non lo è allora redirect alla pagina di login
                return render_template('login.html', flag=True)
            # return redirect(url_for('login'), msgQuit="You're not  logged in.")
        except KeyError:
            return render_template('notLoggedIn.html')
        

    def convert_audio_to_text(audio_file):
        r = sr.Recognizer()


        # # Converti il file MP3 in WAV utilizzando pydub
        # audio = AudioSegment.from_mp3(audio_file)
        # audio.export("audio.wav", format="wav")

        with sr.AudioFile("temp/audio.wav") as source:
            audio = r.record(source)  # Legge l'audio dal file WAV

        try:
            text = r.recognize_google(audio, language='it-IT')  # Converte l'audio in testo
            return text
        except sr.UnknownValueError:
            print("Impossibile riconoscere l'audio.")
        except sr.RequestError as e:
            print(f"Errore durante la richiesta al servizio di riconoscimento vocale di Google: {e}")


    def InserimentoNotiziaAudio(self):
        try:
            # Controllo se l'utente è loggato
            if 'loggedin' in session and session['loggedin']:
                plainAudio = None

                # Verifico che il metodo della richiesta HTTP sia POST
                if request.method == 'POST':
                    # Recupero il contenuto del file audio
                    plainAudio = request.files['audio']
                    
                    # Salvo il file audio
                    audio_path = 'temp/audio.wav'  # Specifica il percorso di destinazione desiderato
                    plainAudio.save(audio_path)
                    
                    
                    # Estrazione vocal to text
                    testo = vistaUtente.convert_audio_to_text(audio_path)  # Sostituisci con la tua funzione di estrazione del testo dall'audio

                    self.miaNotiziaAudio = Audio(0, '', '', testo, '')

                    
                    file_to_rem = pathlib.Path("temp/audio.wav")
                    file_to_rem.unlink()
                    

                    # Verifico se l'utente ha richiesto di calcolare l'indice della notizia testuale
                    if request.form.get('calcolaIndice') is not None:
                        return vistaUtente.VerificaAttendibilita(self.miaNotiziaAudio)

                    # Verifico se l'utente ha richiesto di mostrare fonti attendibili
                    if request.form.get('fontiAttendibili') is not None:
                        return vistaUtente.individuaFontiAttendibili(self.miaNotiziaAudio)
                    
                    
                else:
                    # Reindirizzo alla pagina
                    return render_template('notiziaAudio.html')
            else:
                # Se l'utente non è loggato, redirect alla pagina di login
                return render_template('login.html', flag=True)
        except KeyError:
            return render_template('notLoggedIn.html')

        


    def InserimentoNotiziaVideo(self):
        try:
            # Controllo se l'utente è loggato
            if 'loggedin' in session and session['loggedin']:
                plainVideo = None

                # Verifico che il metodo della richiesta HTTP si POSt
                if request.method == 'POST':
                    # Recupero il contenuto della textArea dell form cioè la notizia inserita dall'utente
                    plainVideo = request.form['inputVideo']

                    self.download_360p_mp4_videos(plainVideo,"temp/Video") 


                    # Controllo che l'unente ha inserito qualcosa, se non lo ha fatto stampo messaggio di errore
                    if plainVideo == '':
                        errore = 'si prega di inserire un url'
                        return render_template('notiziaVideo.html', errore=errore)

                    else:

                        # Controllo se l'utente ha inserito un URL
                        if validators.url(plainVideo) is True:
                            self.miaNotiziaVideo = Video(0, '','', plainVideo, '')
                        else:
                            errore = 'si prega di inserire un url'
                            return render_template('notiziaVideo.html', errore=errore)

                        # Verifico che l'utente ha richiesto di calcolare l'indice dell'immagine
                        if request.form.get('calcolaIndice') is not None:
                            return vistaUtente.VerificaAttendibilita(self.miaNotiziaVideo)
                        
                        # Verifico che l'utente ha richiesto di mostrate fonti attendibili
                        if request.form.get('fontiAttendibili') is not None:
                            # Verifico che l'utente ha richiesto di mostrate fonti attendibili
                            return vistaUtente.individuaFontiAttendibili(self.miaNotiziaVideo)

                else:
                    # Reindirizzo alla pagina
                    return render_template('notiziaVideo.html')

            else:
                # Se non lo è allora redirect alla pagina di login
                return render_template('login.html', flag=True)
            # return redirect(url_for('login'), msgQuit="You're not  logged in.")
        except KeyError:
            return render_template('notLoggedIn.html')
        

    def download_360p_mp4_videos(self,url: str, outpath: str = "./"):    

        yt = YouTube(url)
        yt.streams.filter(file_extension="mp4").get_by_resolution("360p").download(outpath)

    
    def segnalaNotizia(self):
        try:
            # Controllo se l'utente è loggato
            if 'loggedin' in session and session['loggedin']:
                # Verifico che il metodo della richiesta HTTP si POSt
                if request.method == 'POST':
                    if (request.path == "/notiziaTesto/segnalaNotizia"):
                        notiziatesto = NotiziaTestuale(0,"",request.form['titoloSegnalazione'],request.form['urlSegnalazione'],request.form['titoloSegnalazione'])
                        controllerSegnalazione = GestioneSegnalazione(notiziatesto)
                        controllerSegnalazione.esisteSegnalazione()
                        return render_template('notiziaTesto.html',messSegnalazione=1)
                    
                    elif (request.path == "/notiziaImmagine/segnalaNotizia"):

                        immagine = Immagine(0,"","",request.form['urlSegnalazione'],"","","")
                        controllerSegnalazione = GestioneSegnalazione(immagine)
                        controllerSegnalazione.esisteSegnalazione()
                        return render_template('notiziaImmagine.html',messSegnalazione=1)
                    
                    elif (request.path == "/notiziaAudio/segnalaNotizia"):

                        audio = Audio(0,"","",request.form['titoloSegnalazione'],"")
                        controllerSegnalazione = GestioneSegnalazione(audio)
                        controllerSegnalazione.esisteSegnalazione()
                        return render_template('notiziaAudio.html',messSegnalazione=1)
                    
                    elif (request.path == "/notiziaVideo/segnalaNotizia"):
                        print(request.form['urlSegnalazione'])
                        video = Video(0,"","",request.form['urlSegnalazione'],"")
                        controllerSegnalazione = GestioneSegnalazione(video)
                        controllerSegnalazione.esisteSegnalazione()
                        return render_template('notiziaVideo.html',messSegnalazione=1)
                else:
                    # Reindirizzo alla pagina
                    return render_template('notiziaTesto.html')
            else:
                # Se non lo è allora redirect alla pagina di login
                return render_template('login.html')
        # return redirect(url_for('login'), msgQuit="You're not  logged in.")
        except KeyError:
                return render_template('notLoggedIn.html')
        return