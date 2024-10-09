CREATE DATABASE SPROCTOR;

USE SPROCTOR;

CREATE TABLE HeadMovements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    session_id VARCHAR(50) NOT NULL,
    look_up FLOAT DEFAULT 0,
    look_down FLOAT DEFAULT 0,
    look_left FLOAT DEFAULT 0,
    look_right FLOAT DEFAULT 0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Continue inserting the rest of the sample records
INSERT INTO HeadMovements (student_id, session_id, look_up, look_down, look_left, look_right) 
VALUES 
('STU092', 'SESSION010', 2.0, 3.0, 1.5, 2.5),
('STU093', 'SESSION010', 1.0, 2.5, 3.0, 1.5),
('STU094', 'SESSION010', 3.0, 1.0, 2.5, 2.0),
('STU095', 'SESSION010', 2.5, 2.0, 1.0, 3.5),
('STU096', 'SESSION010', 3.0, 1.5, 3.5, 2.0),
('STU097', 'SESSION010', 1.5, 2.5, 2.0, 1.5),
('STU098', 'SESSION010', 2.0, 3.0, 1.5, 3.0),
('STU099', 'SESSION010', 3.5, 2.5, 1.0, 2.0),
('STU100', 'SESSION010', 1.0, 1.5, 2.5, 3.5);
('STU102', 'SESSION010', 3.0, 1.5, 2.5, 1.0),
('STU103', 'SESSION010', 1.0, 3.5, 2.0, 2.5),
('STU104', 'SESSION010', 2.0, 1.0, 3.0, 2.5),
('STU105', 'SESSION010', 3.5, 2.0, 1.5, 1.0),
('STU106', 'SESSION010', 1.5, 3.0, 2.5, 3.0),
('STU107', 'SESSION010', 2.0, 2.5, 3.5, 1.0),
('STU108', 'SESSION010', 3.0, 1.0, 1.0, 2.5),
('STU109', 'SESSION010', 1.0, 2.0, 2.0, 3.5),
('STU110', 'SESSION010', 2.5, 3.5, 1.5, 1.5);
