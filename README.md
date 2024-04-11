<html>
<body>
<h1> 📰 Misinformation Fight System</h1>
<p>Il sistema software <i>"MISINFORMATION FIGHT SYSTEM"</i> ha come obiettivo analizzare e stabilire la veridicità di notizie multimediali per contrastare la rapida diffusione di fake news.<br>
Ogni utente del sistema software potrà fornire in input una notizia in forma multimediale: un testo, un video, un’immagine oppure una traccia audio.
<br>Il sistema utilizzerà diversi criteri per verificare la veridicità di una notizia per esempio identificare i soggetti coinvolti oppure effettuare dei controlli sulla fonte della notizia in questione.<br>
Si prevede inoltre un sistema di segnalazione che permette all'utente di segnalare una notizia da lui ritenuta falsa, queste segnalazioni saranno gestite dal software, ove fossero ingenti si procederà alla verifica della notizia in questione, in questo modo le capacità del sistema miglioreranno grazie all’aiuto dell’utente.<br>
Il software procede a fornire un rating di attendibilità della notizia oltre ad una spiegazione che la supporti. <br>Per aiutare l’utente nella lotta alla disinformazione il sistema fornisce ulteriori fonti e notizie ritenute attendibili. 
</p>



<h1>🌐 Collaborators:</h1>
<ul>
	<li>Antonio Vitale 
 	<a href="https://github.com/vitalelele">
<img src="https://img.shields.io/badge/GitHub-100000?logo=github&logoColor=white" alt="GitHub" style="max-width: 100%;">
  	</a>
   </li>
   	<li>Angelo Sciarra 
 	<a href="https://github.com/Angelo-Sciarra">
<img src="https://img.shields.io/badge/GitHub-100000?logo=github&logoColor=white" alt="GitHub" style="max-width: 100%;">
  	</a>
   </li>
	<li>Michele Minervini
 	<a href="https://github.com/MicheleMinervini06">
<img src="https://img.shields.io/badge/GitHub-100000?logo=github&logoColor=white" alt="GitHub" style="max-width: 100%;">
  	</a>
   </li>
   	<li>Emanuele Piemontese
 	 	<a href="https://github.com/EmanuelePiemontese">
<img src="https://img.shields.io/badge/GitHub-100000?logo=github&logoColor=white" alt="GitHub" style="max-width: 100%;">
  	</a>
		
   </li>

	
</ul>


<h1>👨‍💻 Come eseguire il software:</h1>
<p>
Per esguire il codice bisogna aver installato sul proprio computer Python (consigliabile la versione 3.10.9). 
Per installare python consultare la guida: <i>https://www.python.org/downloads/</i><br>
Dopo aver installato python consigliamo di creare e attivare un ambiente virtuale seguendo questi passaggi:
</p>

Da terminale, nella directory del programma, eseguire: <i>python3 -m venv venv</i>

Attivare l'ambiente virtuale: <br><br>
<b>Windows</b> 
	
	venv\Scripts\activate
	
<b>MacOS\Linux</b> 	
		
	source venv/bin/activate

  <br>

  <p>Per installare le librerie necessarie al funzionamento, posizionarsi all'interno della cartella di Misiformation Fight System e lanciare il seguente comando:</p>

  	pip install -r requirements.txt
		
 <p>Le librerie utilizzate singolarmente sono le seguenti:</p>
 
 	Flask: 
  		pip install flask
	pymysql: 
 		pip install pymysql
	GoogleNews: 
 		pip install GoogleNews
	Requests: 
 		pip install requests
	Spacy: 
 		pip install spacy
	Pacchetto italiano spacy: 
 		python -m spacy download it_core_news_sm
	Googletrans: 
 		pip install googletrans==3.1.0a0
	Transformers: 
 		pip install transformers
	Validators: 
 		pip install validators
	TensorFlow: 
 		pip install TensorFlow 
	PyTorch: 
 		pip install torch
	Google Search Results: 
 		pip install google-search-results
	Pillow: 
 		pip install pillow
	Pydub: 
 		pip install pydub
	Speech Recognition: 
 		pip install SpeechRecognition
	Pathlib: 
 		pip install pathlib
	Pytube: 
 		pip install pytube
	Openc Cv: 
 		pip install opencv-python
   
<p>Successivamente bisogna installare il DBMS MySQL: <p>
	https://dev.mysql.com/downloads/mysql/
 
<p>Installato MySQL si dovrà eseguire lo script per creare il database dell'applicazione:</p>
<ol>
<li> Avviare il server MySQL </li>
<li> Da terminale lanciare il comando:  
	
	mysql -u root -p 
 
<li> Lanciare il comando (<i>utilizzando il vostro percorso per il file</i>): 
	
	source path/to/script/file/misinformationfightsystem.sql;
<li> Modificare la password nel file <i>dataAccessObject.py</i> </li>
 </ol>
<h4>Per esguire l'applicazione utilizzare il seguente comando: </h4>

	python app.py
</body>
</html>


