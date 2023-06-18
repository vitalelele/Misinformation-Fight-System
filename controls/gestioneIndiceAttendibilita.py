from models.notiziaTestuale import NotiziaTestuale
from models.immagine import Immagine
from models.audio import Audio
from models.video import Video
from dataAccessObject import DataAccessObject
from googletrans import Translator
from transformers import pipeline
import requests
from bs4 import BeautifulSoup
from PIL import Image
import cv2
from pathlib import Path


class GestioneIndiceAttendibilita():
    def calcoloIndiceTesto(self, notizia: NotiziaTestuale):
        indiceAttendibilita = []
        criteri = [0]

        contenuto = notizia.getContenuto()
        url = notizia.getUrl()
        titolo = notizia.getTitolo()

        # FactCheck Google
        api_key = "AIzaSyC6OG_GxkjZuH36X31UdzWopzM6Dq0tjJ0"
        # Esegui la richiesta API di Google Fact Check
        # Definizione  della query e inoltro della richiesta HTTP
        query = contenuto
        urlRequest = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={query}&key={api_key}"
        response = requests.get(urlRequest)
        data = response.json()

        # Estrazione dei risultati dalla risposta
        if 'claims' in data:
            claims = data['claims']
            if claims:
                claim = claims[0]
                claim_rating = claim['claimReview'][0]['textualRating']
                claim_autore = claim['claimReview'][0]['publisher']['name']
                risultato = claim_rating
            else:
                risultato = "Nessun risultato trovato."
        else:
            risultato = "Errore nella richiesta."

        indiceAttendibilita.append(-1)
        criteri.append(risultato)

        # starti modello
        # pip install googletrans==3.1.0a0
        # Analisi testuale
        # Scelta del modello
        MODEL = "jy46604790/Fake-News-Bert-Detect"
        clf = pipeline("text-classification", model=MODEL, tokenizer=MODEL)
        # Analiso del testo
        translator = Translator()
        print(type(contenuto))
        translated_text = translator.translate(contenuto)
        text = translated_text.text
        result = clf(text)
        # Elaborazione del risultato
        if (result[0]["label"] == "LABEL_0"):
            indiceAttendibilita.append(1 - result[0]["score"])
        else:
            indiceAttendibilita.append(result[0]["score"])
        if (indiceAttendibilita[1] >= 0 and indiceAttendibilita[1] < 0.35):
            criteri.append("la notizia risulta essere probabilmente falsa")
        elif (indiceAttendibilita[1] >= 0.35 and indiceAttendibilita[1] < 0.7):
            criteri.append(
                "la veridicità della notizia non può essere determinata con certezza")
        else:
            criteri.append("la notizia risulta essere probabimente vera")
        # fine modello

        # Controllo URL
        if url != None:
            api_key = "3fe77a54fad1d7fb037f1a0fcf68a9a1244c6be87e351b36ef0bb5fcac8f265e"
            # Definizione  della query e inoltro della richiesta HTTP
            url_report_url = f"https://www.virustotal.com/vtapi/v2/url/report?apikey={api_key}&resource={url}"
            response = requests.get(url_report_url)
            data = response.json()

            # Estrazione dei risultati dalla risposta
            if response.status_code == 200:
                if data["response_code"] == 1:
                    criteri.append("L'URL è sicuro.")
                    indiceAttendibilita.append(0.7)
                elif data["response_code"] == -2:
                    criteri.append("L'URL è ancora in fase di elaborazione.")
                    indiceAttendibilita.append(0.4)
                else:
                    criteri.append("L'URL è potenzialmente pericoloso.")
                    indiceAttendibilita.append(0.2)
            else:
                criteri.append(
                    "Non è stato possibile analizzare l'URL della notizia")
                indiceAttendibilita.append(-1)
        else:
            criteri.append("Non è stato inserito nessun url")

        # Verifica presenza notizia su Bufale.net
        numeroPagine = 3
        notizieEstratte = []

        # URL della pagina web da cui estrarre le informazioni
        for i in range(2, numeroPagine+1):
            url = f"https://www.bufale.net/bufala/page/{i}/"
            # Effettua la richiesta GET alla pagina web
            response = requests.get(url)

            # Controlla se la richiesta ha avuto successo
            if response.status_code == 200:
                # Crea un oggetto BeautifulSoup a partire dal contenuto HTML della pagina
                soup = BeautifulSoup(response.content, 'html.parser')

                # Estrazione del titolo delle notizie
                elements = soup.find_all(class_='title')
                for element in elements:
                    notizieEstratte.append(element.text)
            else:
                notizieEstratte = "Error"
                break

        if (notizieEstratte != "Error"):
            trovato = 0
            for titolo in notizieEstratte:
                if (titolo.strip() == contenuto.strip()):
                    indiceAttendibilita.append(0.1)
                    criteri.append(
                        "La notizia è stata smentita dal sito di debunking: Bufale.net")
                    trovato = 1
                    break

            if trovato == 0:
                indiceAttendibilita.append(0.5)
                criteri.append(
                    "La notizia non è stata smentita da alcun sito di debunking analizzato")
        else:
            indiceAttendibilita.append(-1)
            criteri.append(
                "Non è stato possibile verificare la presenza della notizia su siti di debunking")

        self.__indiceComplessivo(criteri, indiceAttendibilita)
        
        dbAccessObject = DataAccessObject()
        segnalazioni = dbAccessObject.leggiDatabase("SELECT counter FROM segnalazioni WHERE (contenutoNotizia = %s OR urlNotizia = %s) AND confermato = true",(contenuto,url))

        if segnalazioni:
            for i in range(segnalazioni[0]['counter']):
                criteri[0] = criteri[0] - (criteri[0]*0.05)
            criteri[0] = int(criteri[0])
            criteri.append(
                f"La notizia è stata segnalata {segnalazioni[0]['counter']} volte")
        else:
            criteri.append(
                "La notizia non è stata segnalata")
        return criteri

    def __indiceComplessivo(self, criteri, indiceAttendibilita):
        # Calcolo indice di attendibilità complessivo come media dei sigoli indici
        count = 0
        indiceAttendibilitaComplessivo = 0
        for indice in indiceAttendibilita:
            if (indice != -1):
                count += 1
                indiceAttendibilitaComplessivo += indice
        indiceAttendibilitaComplessivo /= count

        # L'indice di attendibilità viene restituito come valore nell'intervallo [0,100]
        indiceAttendibilitaComplessivo = round(indiceAttendibilitaComplessivo*100)
        criteri[0] = indiceAttendibilitaComplessivo

        return


    def calcoloIndiceImmagine(self, notizia:Immagine):

        indiceAttendibilita = []
        criteri = [0]

        MODEL = "umm-maybe/AI-image-detector"
        clf = pipeline("image-classification", model=MODEL)

        url = notizia.getUrl()

        im = Image.open(requests.get(url, stream=True).raw)

        result = clf(im)

        if(result[0]['label'] == 'artificial'):
            indiceAttendibilita.append(result[1]['score'])
        else:
            indiceAttendibilita.append(result[0]['score'])

        if(indiceAttendibilita[0] >= 0 and indiceAttendibilita[0] < 0.35):
            criteri.append("Utilizzando un modello di anlisi l'immagine risulta essere probabilmente falsa")
        elif(indiceAttendibilita[0] >= 0.35 and indiceAttendibilita[0] < 0.7):
            criteri.append("Utilizzando un modello di anlisi sull'immagine, la sua veridicità non può essere determinata con certezza")
        else:
            criteri.append("Utilizzando un modello di anlisi l'immagine risulta essere probabimente vera")

        self.__indiceComplessivo(criteri, indiceAttendibilita)

        dbAccessObject = DataAccessObject()
        segnalazioni = dbAccessObject.leggiDatabase("SELECT counter FROM segnalazioni WHERE urlNotizia = %s AND confermato = true",(url))

        if segnalazioni:
            for i in range(segnalazioni[0]['counter']):
                criteri[0] = criteri[0] - (criteri[0]*0.05)
            criteri[0] = int(criteri[0])
            criteri.append(
                f"La notizia è stata segnalata {segnalazioni[0]['counter']} volte")
        else:
            criteri.append(
                "La notizia non è stata segnalata")
        return criteri

    def calcoloIndiceAudio(self, notizia:Audio):

        # Creo una notizia testuale con il contenuto della notizia audio
        miaNotiziaTesto = NotiziaTestuale(0, '', notizia.getContenuto(), None, '')
        return self.calcoloIndiceTesto(miaNotiziaTesto)


    def calcoloIndiceVideo(self, notizia:Video):

        for path in Path("temp/Video").iterdir():
            GestioneIndiceAttendibilita.extractImages(str(path),'temp/Video/frame')

        indiceAttendibilita = []
        criteri = [0]

        MODEL = "umm-maybe/AI-image-detector"
        clf = pipeline("image-classification", model=MODEL)

        directory = 'temp/Video/frame'

        for path in Path(directory).iterdir():
            print(path)
            print(directory + '/.DS_Store')
            if str(path) == str(directory + '/.DS_Store'):
                continue
            result = clf(str(path))
            if(result[0]['label'] == 'artificial'):
                indiceAttendibilita.append(result[1]['score'])
            else:
                indiceAttendibilita.append(result[0]['score'])

        if(indiceAttendibilita[0] >= 0 and indiceAttendibilita[0] < 0.35):
            criteri.append("Utilizzando un modello di anlisi il video risulta essere probabilmente falso")
        elif(indiceAttendibilita[0] >= 0.35 and indiceAttendibilita[0] < 0.7):
            criteri.append("Utilizzando un modello di anlisi sul video, la sua veridicità non può essere determinata con certezza")
        else:
            criteri.append("Utilizzando un modello di anlisi il video risulta essere probabimente vero")

        criteri[0] = int((sum(indiceAttendibilita)/len(indiceAttendibilita))*100)

        dbAccessObject = DataAccessObject()
        segnalazioni = dbAccessObject.leggiDatabase("SELECT counter FROM segnalazioni WHERE urlNotizia = %s AND confermato = true",(notizia.getUrl()))

        if segnalazioni:
            for i in range(segnalazioni[0]['counter']):
                criteri[0] = criteri[0] - (criteri[0]*0.05)
            criteri[0] = int(criteri[0])
            criteri.append(
                f"La notizia è stata segnalata {segnalazioni[0]['counter']} volte")
        else:
            criteri.append(
                "La notizia non è stata segnalata")
        return criteri
    


    def extractImages(pathIn, pathOut):

        count = 0
        vidcap = cv2.VideoCapture(pathIn)
        success,image = vidcap.read()
        success = True

        while success:
            vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*10000))# added this line
            success,image = vidcap.read()

            if not success:
                break

            cv2.imwrite( pathOut + "/frame%d.jpg" % count, image)# save frame as JPEG file
            count = count + 1
