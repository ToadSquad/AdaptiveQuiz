
#Dyamic Questions
USE mysql;
LOAD DATA LOCAL INFILE 'C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\dyamicQuestions.csv' #Change Path 
INTO TABLE dynamicQuestions 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS; #ignores header row

#dataDynamicQuestions
USE mysql;
LOAD DATA LOCAL INFILE 'C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\DataDyamicQuestions.csv' #Change Path 
INTO TABLE dataDynamicQuestions 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS; #ignores header row

SHOW VARIABLES LIKE "secure_file_priv";