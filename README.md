<h1>Misinformation Fight System</h1>
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


<h1>🌐 Collaborators:</h1>
<ul>
	<li>Antonio Vitale 
 	<a href="https://github.com/vitalelele">
		<img src="https://camo.githubusercontent.com/8fdc8a65f5384d2285b19d3985fa80f21c23634c6de3a0f0d2aff988c96bef9f/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4769744875622d3130303030303f6c6f676f3d676974687562266c6f676f436f6c6f723d7768697465" alt="Github" data-canonical-src="https://img.shields.io/badge/GitHub-100000?logo=github&amp;logoColor=white" style="max-width: 100%;">
  	</a>
   </li>
   	<li>Angelo Sciarra 
 	<a href="https://github.com/Angelo-Sciarra">
		<img src="https://camo.githubusercontent.com/8fdc8a65f5384d2285b19d3985fa80f21c23634c6de3a0f0d2aff988c96bef9f/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4769744875622d3130303030303f6c6f676f3d676974687562266c6f676f436f6c6f723d7768697465" alt="Github" data-canonical-src="https://img.shields.io/badge/GitHub-100000?logo=github&amp;logoColor=white" style="max-width: 100%;">
  	</a>
   </li>
	<li>Michele Minervini
 	<a href="https://github.com/MicheleMinervini06">
		<img src="https://camo.githubusercontent.com/8fdc8a65f5384d2285b19d3985fa80f21c23634c6de3a0f0d2aff988c96bef9f/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4769744875622d3130303030303f6c6f676f3d676974687562266c6f676f436f6c6f723d7768697465" alt="Github" data-canonical-src="https://img.shields.io/badge/GitHub-100000?logo=github&amp;logoColor=white" style="max-width: 100%;">
  	</a>
   </li>
   	<li>Emanuele Piemontese
 	 	<a href="https://github.com/EmanuelePiemontese">
		<img src="https://camo.githubusercontent.com/8fdc8a65f5384d2285b19d3985fa80f21c23634c6de3a0f0d2aff988c96bef9f/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4769744875622d3130303030303f6c6f676f3d676974687562266c6f676f436f6c6f723d7768697465" alt="Github" data-canonical-src="https://img.shields.io/badge/GitHub-100000?logo=github&amp;logoColor=white" style="max-width: 100%;">
  	</a>
		
   </li>

	
</ul>


