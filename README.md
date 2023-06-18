Per esguire il codice bisogna aver isntallato sul proprio computer Python (consigliabile la versione 3.10.9). Per installare python consultare la guida: https://www.python.org/downloads/ .
Dopo aver installato pyhon consigliamo di creare e attiavre un ambiente virtuale seguendo questi passaggi:
1) Da terminale, nella directory del programma, eseguire: python3 -m venv venv
2) Attivare l'ambiente virtuale: 
	-windows: venv\Scripts\activate
	-macOS\Linux: source venv/bin/activate
Attivato l'ambiente virtuale installare le seguneti librerie di python, necessarie per il funzionamento del programma:
	-Flask: pip install flask
	-pymysql: pip install pymysql
	-GoogleNews: pip install GoogleNews
	-Requests: pip install requests
	-Spacy: pip install spacy
	-Pacchetto italiano spacy: python -m spacy download it_core_news_sm
	-Googletrans: pip install googletrans==3.1.0a0
	-Transformers: pip install transformers
	-Validators: pip install validators
	-TensorFlow: pip install TensorFlow 
	-PyTorch: pip install torch
	-Google Search Results: pip install google-search-results
	-Pillow: pip install pillow
	-Pydub: pip install pydub
	-Speech Recognition: pip install SpeechRecognition
	-Pathlib: pip install pathlib
	-Pytube: pip install pytube
	-Openc Cv: pip install opencv-python
Successivamente bisogna installare il DBMS mysql: https://dev.mysql.com/downloads/mysql/
Installato mysql si dovrà eseguire lo script per creare il database dell'applicazione:
	-avviare il server mysql
	-da terminale lanciare il comando:  mysql -u root -p
	-lanciare il comando (utilizzando il vostro percorso per il file): source path/to/script/file/misinformationfightsystem.sql;
	-modificare la password nel file dataAccessObject.py
Per esguire l'applicazione utilizzare il seguente comando: python app.py

