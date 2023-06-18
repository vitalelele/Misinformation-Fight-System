CREATE DATABASE IF NOT EXISTS `misinformationfightsystem` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `misinformationfightsystem`;

CREATE TABLE IF NOT EXISTS `utenti` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
    `nome` varchar(30) NOT NULL,
    `cognome` varchar(30) NOT NULL,
  	`username` varchar(50) NOT NULL,
  	`email` varchar(100) NOT NULL,
    `password` varchar(64) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `giornalisti` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`nome` varchar(30) NOT NULL,
    `cognome` varchar(30) NOT NULL,
    `username` varchar(50) NOT NULL,
    `email` varchar(100) NOT NULL,
    `password` varchar(64) NOT NULL,
    `matricola` varchar(9) NOT NULL UNIQUE,
    `codiceFiscale` varchar(16) NOT NULL,
    `regione` varchar(20) NOT NULL,
    `verificato` BOOLEAN NOT NULL DEFAULT false,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `amministratori` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`nome` varchar(30) NOT NULL,
    `cognome` varchar(30) NOT NULL,
    `username` varchar(50) NOT NULL,
    `email` varchar(100) NOT NULL,
    `password` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `fonti` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`nome` varchar(30) NOT NULL,
    `urlSito` varchar(100) NOT NULL,
    `argomentiTrattati` varchar(40) NOT NULL,
    `attendibile` BOOLEAN NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `segnalazioni` (
	`idSegnalazione` int(11) NOT NULL AUTO_INCREMENT,
    `counter` int(30) NOT NULL,
    `confermato` BOOLEAN NOT NULL DEFAULT false,
  	`contenutoNotizia` varchar(300) NOT NULL,
  	`urlNotizia` varchar(300) NOT NULL,
    `tipo` varchar(50) NOT NULL,
    PRIMARY KEY (`idSegnalazione`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

INSERT INTO `utenti` (`id`,`nome`,`cognome`, `username`, `password`, `email`) VALUES (1, 'Zlatan','Ibrahimovic' ,'test', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 'test@test.com');
INSERT INTO `amministratori` (`id`,`nome`,`cognome`, `username`, `password`, `email`) VALUES (1, 'Antonio','Vitale' ,'admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'admin@admin.com');

INSERT INTO `fonti` (`nome`,`urlsito`, `argomentiTrattati`, `attendibile`) VALUES ('Corriere della Sera','https://www.corriere.it/' ,'attualita', True);
INSERT INTO `fonti` (`nome`,`urlsito`, `argomentiTrattati`, `attendibile`) VALUES ('L\'espresso','http://www.espressonline.it' ,'attualitàIntrattenimento', True);
INSERT INTO `fonti` (`nome`,`urlsito`, `argomentiTrattati`, `attendibile`) VALUES ('Panorama','https://www.panorama.it/' ,'attualitàIntrattenimento', True);
INSERT INTO `fonti` (`nome`,`urlsito`, `argomentiTrattati`, `attendibile`) VALUES ('Famiglia Cristiana','https://www.famigliacristiana.it/','attualitàIntrattenimento', True);
INSERT INTO `fonti` (`nome`,`urlsito`, `argomentiTrattati`, `attendibile`) VALUES ('La repubblica','https://www.repubblica.it/' ,'attualitàIntrattenimento', True);
INSERT INTO `fonti` (`nome`,`urlsito`, `argomentiTrattati`, `attendibile`) VALUES ('La Stampa','https://www.lastampa.it/' ,'attualitàIntrattenimento', True);
INSERT INTO `fonti` (`nome`,`urlsito`, `argomentiTrattati`, `attendibile`) VALUES ('Libero Quotidiano','https://www.liberoquotidiano.it/' ,'attualitàIntrattenimento', True);
INSERT INTO `fonti` (`nome`,`urlsito`, `argomentiTrattati`, `attendibile`) VALUES ('Ansa','https://www.ansa.it/' ,'Attualita e Infromzione', True);
INSERT INTO `fonti` (`nome`,`urlsito`, `argomentiTrattati`, `attendibile`) VALUES ('La Gazzetta dello Sport','https://www.gazzetta.it/' ,'sport', True);
INSERT INTO `fonti` (`nome`,`urlsito`, `argomentiTrattati`, `attendibile`) VALUES ('Corriere dello Sport','https://www.corrieredellosport.it/' ,'sport', True);
INSERT INTO `fonti` (`nome`,`urlsito`, `argomentiTrattati`, `attendibile`) VALUES ('Tuttosport','https://www.tuttosport.com/' ,'sport', True);
INSERT INTO `fonti` (`nome`,`urlsito`, `argomentiTrattati`, `attendibile`) VALUES ('Equiqe','https://www.lequipe.fr/' ,'sport', True);
INSERT INTO `fonti` (`nome`,`urlsito`, `argomentiTrattati`, `attendibile`) VALUES ('Marca','https://www.marca.com/' ,'sport', True);
INSERT INTO `fonti` (`nome`,`urlsito`, `argomentiTrattati`, `attendibile`) VALUES ('National Geographic Italia','https://www.nationalgeographic.it/' ,'scienza', True);
INSERT INTO `fonti` (`nome`,`urlsito`, `argomentiTrattati`, `attendibile`) VALUES ('Focus','https://www.focus.it/' ,'scienza', True);
INSERT INTO `fonti` (`nome`,`urlsito`, `argomentiTrattati`, `attendibile`) VALUES ('Il Sole 24 Ore','https://www.ilsole24ore.com/','economia', True);
INSERT INTO `fonti` (`nome`,`urlsito`, `argomentiTrattati`, `attendibile`) VALUES ('Milano Finanza','https://www.milanofinanza.it/' ,'economia', True);
INSERT INTO `fonti` (`nome`,`urlsito`, `argomentiTrattati`, `attendibile`) VALUES ('Italia Oggi','https://www.italiaoggi.it/' ,'economia', True);
INSERT INTO `fonti` (`nome`,`urlsito`, `argomentiTrattati`, `attendibile`) VALUES ('Tom\'s Hardware','https://www.tomshw.it/' ,'Informatica', True);



-- 
/*
In SHA256()
8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918 --> admin
9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08 --> test
*/
USE `misinformationfightsystem`;
INSERT INTO `giornalisti` (`nome`,`cognome`, `username`, `password`, `email`, `matricola`, `codiceFiscale`, `regione`, `verificato`) VALUES ('Mario', 'Rossi', 'mariorossi23', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 'mariorossi@gmail.com', '756420T' , 'THBSDG32S25E356P', 'Puglia', false);
INSERT INTO `giornalisti` (`nome`,`cognome`, `username`, `password`, `email`, `matricola`, `codiceFiscale`, `regione`, `verificato`) VALUES ('Paolo', 'Neri', 'paoloneri46', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 'paoloneri@gmail.com', '432147F' , 'SNVFZN51R49E393U', 'Liguria', false); 