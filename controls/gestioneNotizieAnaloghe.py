from models.notiziaTestuale import NotiziaTestuale
from models.immagine import Immagine
from models.notizia import Notizia
from GoogleNews import GoogleNews
from PIL import Image
from serpapi import GoogleSearch
import requests
import spacy

class GestioneNotizieAnaloghe:

    def __init__(self,notizia : Notizia) -> None:
        self.__notizia = notizia

    def notizieAnalogheTesto(self):
        # Variabile che conterrÃ  le notizie simili trovate
        news_results = None
        notizieAnaloghe = []
        parolechiave = self.elementiDistintivi()
        googlenews = GoogleNews(lang='it', region='it')
        googlenews.search(self.__notizia.getTitolo())
        # Ottenere i risultati della ricerca
        news_results = googlenews.results()
        
        if news_results != None:
            # Se ho trovato delle notizie crea una lista di notizie Testuali con i dati delle notizie trovate
            for news in news_results:
                notizieAnaloghe.append(NotiziaTestuale(0,'',news['title'],news['link'],news['desc']))
        return notizieAnaloghe
    
    def elementiDistintivi(self):
        nlp = spacy.load('it_core_news_sm')
        if self.__notizia.getContenuto():
            doc = nlp(self.__notizia.getContenuto())
        else:
            doc = nlp(self.__notizia.getTitolo())

        query = ""
        for sentence in doc.sents:
            subject = ''
            verb = ''
            object_ = ''

            for token in sentence:
                if 'subj' in token.dep_:
                    subject = token.text
                elif 'obj' in token.dep_:
                    object_ = token.text
                elif 'ROOT' in token.dep_:
                    verb = token.text
                if subject:
                    query += f" {subject}"
                    if verb:
                        query += f" {verb}"
                    if object_:
                        query += f" {object_}"
                elif verb:
                    query += verb
                    if object_:
                        query += f" {object_}"
                if object_:
                    query += f" {object_}"
        return query
    

    def notizieAnalogheImmagine(self):

        notizieAnaloghe = []
        url = self.__notizia.getUrl()

        params = {
            "engine": "google_lens",
            "url": url,
            "api_key": "1868da6313f6e9052ef6fe0c4fd25bd86bda2d0a70bd67b1233ed9e7fef8e951",
            "hl": "it"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        visual_matches = results["visual_matches"]

        if len(visual_matches) > 6:
            num_images = 6
        else:
            num_images = len(visual_matches)

        for i in range(num_images):
            foto1 = visual_matches[i]["thumbnail"]
            descrizione = visual_matches[i]["link"]
            im = Image.open(requests.get(foto1, stream=True).raw)
            notizieAnaloghe.append(Immagine(0, '', '', foto1, descrizione, '', ''))

        return notizieAnaloghe
    
    def notizieAnalogheAudio(self):
        miaNotiziaTestuale = NotiziaTestuale(0, '', self.__notizia.getContenuto(), '', self.__notizia.getContenuto())
        self.__notizia = miaNotiziaTestuale
        return self.notizieAnalogheTesto()
