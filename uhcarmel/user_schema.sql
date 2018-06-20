CREATE TABLE IF NOT EXISTS `user` (
   `id` int(11) NOT NULL AUTO_INCREMENT,
   `mirs` varchar(10) NOT NULL,
   `password_hash` varchar(100) NOT NULL,
   `first_name` varchar(50) NOT NULL,
   `last_name` varchar(50) NOT NULL,
   `google_sid` varchar(100) DEFAULT NULL,
   `google_email` varchar(100) DEFAULT NULL,
   `is_manager` tinyint(1) DEFAULT NULL,
   `address` varchar(250) NOT NULL,
   `city` varchar(100) NOT NULL,
   PRIMARY KEY (`id`),
   UNIQUE KEY `IDX_MIRS` (`mirs`)
 ) DEFAULT CHARSET=utf8;