
USE mysql;
#Question Table
CREATE TABLE question (prompt VARCHAR(250), option1 VARCHAR(250), option2 VARCHAR(250), option3 VARCHAR(250),  option4 VARCHAR(250),  option5 VARCHAR(250), option6 VARCHAR(250), answer VARCHAR(250), category VARCHAR(20),diffuculty INT);

#User Table
CREATE TABLE users (playername VARCHAR(20), username VARCHAR(20), playerpassword VARCHAR(20), highscore INT);

#User Data
USE mysql;
CREATE TABLE userData (id INT NOT NULL AUTO_INCREMENT, prompt VARCHAR(250), category VARCHAR(20), lengthTime INT, username VARCHAR(20), correct BOOL, PRIMARY KEY (Personid));