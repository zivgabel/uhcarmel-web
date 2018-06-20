CREATE TABLE IF NOT EXISTS `location` (
   `id` int(11) NOT NULL AUTO_INCREMENT,
   `name` varchar(250) NOT NULL,
   `altitude` varchar(250) NOT NULL,
   `longitude` varchar(250) NOT NULL,
   PRIMARY KEY (`id`)
 ) DEFAULT CHARSET=utf8;
