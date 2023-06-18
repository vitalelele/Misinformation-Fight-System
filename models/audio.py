from .notizia import Notizia

# Sottoclasse di notizia, modella la notizia testuale
class Audio(Notizia):
    def __init__(self, indiceAttendibilita, autore, formato, contenuto, data):
        super().__init__(indiceAttendibilita, autore)
        self.__formato = formato
        self.__contenuto = contenuto
        self.__data = data

    def getFormato(self):
        return self.__formato

    def setFormato(self, formato):
        self.__formato = formato

    def getContenuto(self):
        return self.__contenuto

    def setContenuto(self, contenuto):
         self.__contenuto = contenuto

    def getData(self):
        return self.__data

    def setData(self, data):
        self.__data = data