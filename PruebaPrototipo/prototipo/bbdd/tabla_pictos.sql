USE `mcr30`;

CREATE TABLE IF NOT EXISTS `pictogramas` (
  `id_picto` int(10) NOT NULL,
  `imagen` BLOB NOT NULL,
  PRIMARY KEY (`id_picto`)
  
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE IF NOT EXISTS `datos_picto` (
  `palabra` varchar(100) COLLATE utf8_bin NOT NULL,
  `offset31` varchar(17) COLLATE utf8_bin NOT NULL,
  `offset30` varchar(17) COLLATE utf8_bin NOT NULL,
  `id_picto` int(10) NOT NULL,
  PRIMARY KEY (`offset30`, `palabra`,`id_picto`)
  
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


CREATE TABLE IF NOT EXISTS `pictos` (
  `offset30` varchar(17) COLLATE utf8_bin NOT NULL,
  `palabra` varchar(100) COLLATE utf8_bin NOT NULL,
  `id_picto` int(10) NOT NULL,
  `imagen` BLOB,
  PRIMARY KEY (`offset30`, `palabra`,`id_picto`)
  
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
