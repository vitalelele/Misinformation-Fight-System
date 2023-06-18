import spacy
import json
from dataAccessObject import DataAccessObject
from models.notizia import Notizia
from models.notiziaTestuale import NotiziaTestuale
from models.immagine import Immagine
from models.audio import Audio
from models.fonte import Fonte
from googletrans import Translator
from transformers import AutoImageProcessor, ResNetForImageClassification
import torch
import requests
from PIL import Image

class GestioneFontiAttendibili:

    def __init__(self, notizia : NotiziaTestuale) -> None:
        self.__notizia = notizia
    
    def fontiAttendibili(self):
        argomentiTrattati = self.inidviduaArgomenti()
        fontiAttendibili = []
        for argomento in argomentiTrattati:
            dbAccessObject = DataAccessObject()
            fonti = dbAccessObject.leggiDatabase("SELECT nome,urlSito,argomentiTrattati,attendibile FROM fonti WHERE argomentiTrattati = %s AND attendibile = True",(argomento))
            for fonte in fonti:
                fontiAttendibili.append(Fonte(fonte['nome'],fonte['urlSito'],fonte['argomentiTrattati'],fonte['attendibile']))

        return fontiAttendibili

    
    def categoria(self, testo):
            
        # Caricamento del pacchetto linguistico italiano
            nlp = spacy.load('it_core_news_sm')
        
            # Ttokenizzazione del testo
            doc = nlp(testo)

            # Rimozione delle stopwords e trasformazione dei verbi all'inifinito
            tokens_without_stopwords = []
            for token in doc:
                if token.pos_ == 'VERB':
                    tokens_without_stopwords.append(token.lemma_)
                elif not token.is_stop:
                    tokens_without_stopwords.append(token.text)

            # Conto il numero di parole del testo senza stopwords
            numero_parole = len(tokens_without_stopwords)

            argomentiTrattati = []
            coefficenti_parole_categoria = {"sport" : 0, "attualita" : 0, "scienza" : 0, "economia" : 0}

            # Caricamento del dataset di parole usate in articoli di gionale
            with open('parole_argomento.json', 'r', encoding='utf-8') as file:
                # Carica il contenuto JSON dal file
                data = json.load(file)

                occorrenzeParole = {"sport" : 0, "attualita" : 0, "scienza" : 0, "economia" : 0}

                for token in tokens_without_stopwords:
                    for elemento in data['sport']:
                        if token.lower() in elemento or (token.lower() in elemento.split() if ' ' in elemento else False):
                            occorrenzeParole['sport'] += 1
                            break
                    
                    for elemento in data['attualita']:
                        if token.lower() in elemento or (token.lower() in elemento.split() if ' ' in elemento else False):
                            occorrenzeParole['attualita'] += 1
                            break
                    
                    for elemento in data['scienza']:
                        if token.lower() in elemento or (token.lower() in elemento.split() if ' ' in elemento else False):
                            occorrenzeParole['scienza'] += 1
                            break
                    
                    for elemento in data['economia']:
                        if token.lower() in elemento or (token.lower() in elemento.split() if ' ' in elemento else False):
                            occorrenzeParole['economia'] += 1
                            break
                
                
                for key in occorrenzeParole.keys():
                    coefficenti_parole_categoria[key] = occorrenzeParole[key]/numero_parole
                    
                    if coefficenti_parole_categoria[key] > 0:
                        argomentiTrattati.append(key)

            return argomentiTrattati
    
    def inidviduaArgomenti(self):

        # Controllo se la notizia è testuale
        if isinstance(self.__notizia, NotiziaTestuale):
            if self.__notizia.getContenuto():
                testo = self.__notizia.getContenuto()
            elif self.__notizia.getTitolo():
                testo = self.__notizia.getTitolo()
        
            return self.categoria(testo)


        # Controllo se la notizia è testuale
        if isinstance(self.__notizia, Immagine):
            url = self.__notizia.getUrl()

            im = Image.open(requests.get(url, stream=True).raw)

            processor = AutoImageProcessor.from_pretrained("microsoft/resnet-50")
            model = ResNetForImageClassification.from_pretrained("microsoft/resnet-50")

            inputs = processor(im, return_tensors="pt")

            with torch.no_grad():
                logits = model(**inputs).logits

            # Model predicts one of the 1000 ImageNet classes
            predicted_label = logits.argmax(-1).item()
            argomenti_ing = model.config.id2label[predicted_label]
            # print(argomenti_ing)

            translator = Translator()
            argomenti_ita = translator.translate(argomenti_ing, dest='it')
            argomenti_ita = argomenti_ita.text
            # print(argomenti_ita)
            
            return self.categoria(argomenti_ita)
        
        # Controllo se la notizia è testuale
        if isinstance(self.__notizia, Audio):

            miaNotiziaTestuale = NotiziaTestuale(0, '', self.__notizia.getContenuto(), '', '')
            self.__notizia = miaNotiziaTestuale

            if self.__notizia.getContenuto():
                testo = self.__notizia.getContenuto()
            elif self.__notizia.getTitolo():
                testo = self.__notizia.getTitolo()
        
            return self.categoria(testo) 