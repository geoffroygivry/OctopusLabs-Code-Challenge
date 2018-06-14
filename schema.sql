USE wordcloudstore;

DROP TABLE IF EXISTS words;
CREATE TABLE words
(
  encryptedword           varchar(255) NOT NULL,                # Salted hash encryted word
  word                    varchar(255) NOT NULL,                # The word itself
  countedword             decimal(10,2) NOT NULL,               # the number of time the word has been in the title

  PRIMARY KEY     (encryptedword)
);
