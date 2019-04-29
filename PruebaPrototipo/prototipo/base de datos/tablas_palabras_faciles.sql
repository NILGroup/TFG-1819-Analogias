
USE `mcr30`;

CREATE TABLE IF NOT EXISTS `1000_palabras_faciles` (
  `word` varchar(100) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`word`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


CREATE TABLE IF NOT EXISTS `5000_palabras_faciles` (
  `word` varchar(100) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`word`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


CREATE TABLE IF NOT EXISTS `10000_palabras_faciles` (
  `word` varchar(100) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`word`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;