class Fonte:
    def __init__(self, nome, urlSito, argomentiTrattati,attendibile) -> None:
        self.__nome = nome
        self.__urlSito = urlSito
        self.__argomentiTrattati = argomentiTrattati
        self.__attendibilite = attendibile

    def getNome(self):
        return self.__nome
    
    def setNome(self, nome):
        self.__nome = nome

    def getUrlSito(self):
        return self.__urlSito
    
    def setUrlSito(self, urlSito):
        self.__urlSito = urlSito

    def getArgomentiTrattati(self):
        return self.__argomentiTrattati
    
    def setArgomentiTrattati(self, argomentiTrattati):
        self.__argomentiTrattati = argomentiTrattati
    
    def getAttendibile(self):
        return self.__attendibilite
    
    def setAttendibile(self, attendibile):
        self.__argomen__attendibilitetiTrattati = attendibile

    