from .notizia import Notizia

# Sottoclasse di notizia, modella la notizia testuale
class Video(Notizia):
    def __init__(self, indiceAttendibilita, autore, formato, url, data):
        super().__init__(indiceAttendibilita, autore)
        self.__formato = formato
        self.__url = url
        self.__data = data

    def getFormato(self):
        return self.__formato

    def setContenuto(self, contenuto):
        self.__contenuto = contenuto

    def getUrl(self):
        return self.__url

    def setUrl(self, url):
        self.__url = url

    def getData(self):
        return self.__data

    def setData(self, data):
        self.__data = data