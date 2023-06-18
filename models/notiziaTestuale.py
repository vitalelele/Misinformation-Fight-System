from .notizia import Notizia

# Sottoclasse di notizia, modella la notizia testuale
class NotiziaTestuale(Notizia):
    def __init__(self, indiceAttendibilita, autore, contenuto, url, titolo):
        super().__init__(indiceAttendibilita, autore)
        self.__contenuto = contenuto
        self.__url = url
        self.__titolo = titolo

    def getContenuto(self):
        return self.__contenuto

    def setContenuto(self, contenuto):
        self.__contenuto = contenuto

    def getUrl(self):
        return self.__url

    def setUrl(self, url):
        self.__url = url

    def getTitolo(self):
        return self.__titolo

    def setTitolo(self, titolo):
        self.__titolo = titolo

    