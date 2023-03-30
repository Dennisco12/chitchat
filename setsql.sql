-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS chitchat_db;
CREATE USER IF NOT EXISTS 'chit'@'localhost' IDENTIFIED BY 'chitchat_pwd';
GRANT ALL PRIVILEGES ON `chitchat_db`.* TO 'chit'@'localhost';
FLUSH PRIVILEGES;
