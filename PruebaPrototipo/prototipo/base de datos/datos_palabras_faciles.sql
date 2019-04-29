
USE `mcr30`;

LOAD DATA LOCAL INFILE 'C:/Wordnet-BBDD/spaWN/1000_palabras_faciles.csv' INTO TABLE `1000_palabras_faciles` LINES TERMINATED BY '\r\n';
LOAD DATA LOCAL INFILE 'C:/Wordnet-BBDD/spaWN/5000_palabras_faciles.csv' INTO TABLE `5000_palabras_faciles` LINES TERMINATED BY '\r\n';
LOAD DATA LOCAL INFILE 'C:/Wordnet-BBDD/spaWN/10000_palabras_faciles.csv' INTO TABLE `10000_palabras_faciles` LINES TERMINATED BY '\r\n';