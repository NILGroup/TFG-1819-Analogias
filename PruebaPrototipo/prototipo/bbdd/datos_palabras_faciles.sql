
USE `mcr30`;

LOAD DATA LOCAL INFILE 'C:/Wordnet-BBDD/spaWN/1000_palabras_faciles.csv' INTO TABLE `1000_palabras_faciles` FIELDS TERMINATED BY ';' LINES TERMINATED BY '\r\n'(@word, @tag) set word=@word, tag=@tag;
LOAD DATA LOCAL INFILE 'C:/Wordnet-BBDD/spaWN/5000_palabras_faciles.csv' INTO TABLE `5000_palabras_faciles` FIELDS TERMINATED BY ';' LINES TERMINATED BY '\r\n'(@word, @tag) set word=@word, tag=@tag;
LOAD DATA LOCAL INFILE 'C:/Wordnet-BBDD/spaWN/10000_palabras_faciles.csv' INTO TABLE `10000_palabras_faciles` FIELDS TERMINATED BY ';' LINES TERMINATED BY '\r\n'(@word, @tag) set word=@word, tag=@tag;