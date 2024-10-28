CREATE DATABASE UserDB;
USE UserDB;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);

INSERT INTO users (username, password) VALUES
('alice', 'password123'),
('bob', 'securePass456'),
('charlie', 'charliePwd789');
