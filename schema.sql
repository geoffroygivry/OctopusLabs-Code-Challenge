USE wordcloudstore;



-- ****************** SqlDBM: MySQL ******************;
-- ***************************************************;

DROP TABLE IF EXISTS `words`;



-- ************************************** `words`

CREATE TABLE `words`
(
 `encryptedword` VARCHAR(255) NOT NULL ,
  `word`          VARCHAR(255) NOT NULL ,
 `countedword`   INT NOT NULL ,

PRIMARY KEY (`encryptedword`)
);
