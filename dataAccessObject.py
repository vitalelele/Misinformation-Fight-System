import pymysql

class DataAccessObject():
    # Costruttore
    def __init__(self):
        # Settings credenziali database
        self.__conn = pymysql.connect(host="localhost", # host name database
                               user="root",  # username database
                               password="admin", # password per accedere al database
                               db="misinformationfightsystem",  
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor
                               )
    
    def leggiDatabase(self,query : str ,parametri : tuple):
        # Creazione cursore per eseguire la query
        cursor = self.__conn.cursor()

        # Escaping dei parametri
        for parametro in parametri:
              parametro = self.__conn.escape(parametro)
        # Esecuzione query
        cursor.execute(query,parametri)
        # Recupero risultati query
        risultato = cursor.fetchall()
        return risultato
    
    def scritturaDatabase(self,query : str ,parametri : tuple):
        cursor = self.__conn.cursor()

        # Escaping dei parametri
        for parametro in parametri:
              parametro = self.__conn.escape(parametro)
        # Esecuzione query
        cursor.execute(query,parametri)
        
        # Recupero risultati query
        self.__conn.commit()
        return True

    # Distruttore
    def __del__(self):
        self.__conn.close()