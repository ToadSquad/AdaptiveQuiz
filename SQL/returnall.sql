USE mysql;
INSERT INTO question VALUES ("How do you tune the kernel?", "ps -aux", "mount -l | grep nfs", "ifconfig",  "/etc/inittab",  "/etc/exports","df -h", "edit /proc/sys file / Sysctl command", "linux OS");
select * from mysql.question;
select * from mysql.users;
select * from mysql.userData;

UPDATE mysql.question SET diffuculty = 10;

DELETE FROM mysql.question WHERE prompt="test new question";

INSERT INTO userData VALUES ("Which option is not used to access the LINUX system?", "linux OS", 0, "w", False);