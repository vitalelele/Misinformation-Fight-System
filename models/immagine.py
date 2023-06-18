from .notizia import Notizia

#sottoclasse di notizia, modella la notizia immaagine
class Immagine(Notizia):
    def __init__(self, indiceAttendibilita, autore, contenuto, url, descrizione, categoria, data):
        super().__init__(indiceAttendibilita, autore)
        self.__contenuto = contenuto
        self.__url = url
        self.__descrizione = descrizione
        self.__categoria = categoria
        self.__data = data

    def getFormato(self):
        return self.__contenuto

    def setFormato(self, contenuto):
        self.__contenuto = contenuto

    def getUrl(self):
        return self.__url

    def setUrl(self, url):
        self.__url = url

    def getDescrizione(self):
        return self.__descrizione

    def setDescrizione(self, descrizione):
        self.__descrizione = descrizione

    def getCategoria(self):
        return self.__categoria

    def setCategoria(self, categoria):
        self.__categoria = categoria

    def getData(self):
        return self.__data

    def setData(self, data):
        self.__data = data