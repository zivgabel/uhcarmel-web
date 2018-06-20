CREATE TABLE IF NOT EXISTS `pending_user` (
   `id` int(11) NOT NULL AUTO_INCREMENT,
   `google_sid` varchar(100) DEFAULT NULL,
   `google_email` varchar(100) DEFAULT NULL,
   PRIMARY KEY (`id`)
 ) DEFAULT CHARSET=utf8;