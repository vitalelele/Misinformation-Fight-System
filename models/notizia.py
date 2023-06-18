# Classe che modella la notizia elaborata dal sistema
# E' generalizzazione di quattro sottoclassi(NotiziaTestuale, Audio, Immagine, Video)
class Notizia:
    # Costruttore
    def __init__(self, indiceAttendibilita, autore):
        self.__indiceAttendibilita = indiceAttendibilita
        self.__autore = autore

    def getIndiceAttendibilita(self):
        return self.__indiceAttendibilita

    def setIndiceAttendibilita(self, indiceAttendibilita):
        self.__indiceAttendibilita = indiceAttendibilita

    def getAutore(self):
        return self.__autore

    def setAutore(self, autore):
        self.__autore = autore

