CREATE DATABASE IF NOT EXISTS votesysdb;

USE votesysdb;

CREATE TABLE IF NOT EXISTS usertab (
		userid 	INT  UNSIGNED 	NOT NULL AUTO_INCREMENT,
		surname 	VARCHAR(45)		NOT NULL,
		midname    VARCHAR(45),
		firstname 	VARCHAR(45)		NOT NULL,
		regdate 	DATE NOT NULL,
		phone 		VARCHAR(45)		NOT NULL,
		email 		VARCHAR(100) 	NOT NULL UNIQUE,
		pass    	VARCHAR(45)		NOT NULL,
		category 	VARCHAR(45)     NOT NULL,
        PRIMARY KEY (userid)
		)ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1;


CREATE TABLE IF NOT EXISTS loginstamptab (
		loginid 	BIGINT UNSIGNED 	NOT NULL AUTO_INCREMENT,
		userid 		INT UNSIGNED 		NOT NULL,
		logintime 	DATETIME			NOT NULL,
		logouttime 	DATETIME			NOT NULL,
		CONSTRAINT PK_loginstamptab PRIMARY KEY (loginid),
		CONSTRAINT FK_loginstamptab_userid FOREIGN KEY (userid)
		REFERENCES usertab(userid)
		ON UPDATE CASCADE ON DELETE RESTRICT
		)ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1;

UPDATE usertab SET email = 'odukayeabiodun@gmail.com' WHERE userid = 1;
/*
CREATE TABLE IF NOT EXISTS contest_2020_tab (
		contid 		INT  		UNSIGNED 	NOT NULL AUTO_INCREMENT,
		userid 		INT  		UNSIGNED 	NOT NULL,
		surname 	VARCHAR(45)				NOT NULL,
		midname    	VARCHAR(45),
		firstname 	VARCHAR(45)				NOT NULL,
		phone 		VARCHAR(45)				NOT NULL,
		email 		VARCHAR(100) 			NOT NULL UNIQUE,
		position    VARCHAR(45),
        PRIMARY KEY (contid),
		FOREIGN KEY (userid) REFERENCES usertab(userid)
		ON UPDATE CASCADE ON DELETE RESTRICT
		)ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1;
*/

CREATE TABLE IF NOT EXISTS contest_2020_tab (
		contid 		INT  		UNSIGNED 	NOT NULL AUTO_INCREMENT,
		userid 		INT  		UNSIGNED 	NOT NULL,
		position    VARCHAR(45),
        PRIMARY KEY (contid),
		FOREIGN KEY (userid) REFERENCES usertab(userid)
		ON UPDATE CASCADE ON DELETE RESTRICT
		)ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1;

/*Upom supply of these two Do Copy & Paste
/*email
/*position
START TRANSACTION;

INSERT INTO contest_2020_tab (userid)
SELECT userid FROM usertab 
WHERE email='odukayeabiodun@gmail.com';

UPDATE contest_2020_tab 
SET position = 'president' 
WHERE email = 'odukayeabiodun@gmail.com';

COMMIT;