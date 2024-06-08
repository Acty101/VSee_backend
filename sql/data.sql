PRAGMA foreign_keys = ON;

INSERT INTO users(username, name, password, filename, is_vc, points, industry, summary)
VALUES ('aaa', 'Company A', 'password', 'startup_1.jpg', 0, 0, 'Tech', 'wow');

INSERT INTO users(username, name, password, filename, is_vc, points, industry, summary)
VALUES ('bbb', 'Company B', 'password', 'startup_2.jpg', 0, 0, 'Consulting', 'wow');

INSERT INTO users(username, name, password, filename, is_vc, points, industry, summary)
VALUES ('ccc', 'Company C', 'password', 'startup_3.jpg', 0, 0, 'Transportation', 'wow');

INSERT INTO users(username, name, password, filename, is_vc, points, industry, summary)
VALUES ('zzz', 'Investor Z', 'password', 'vc_1.jpg', 1, 0, 'Transportation', 'wow');

INSERT INTO questions(text, is_vc)
VALUES ("Tell me more about yourself", 0) 

INSERT INTO questions(text, is_vc)
VALUES ("What services or products are you selling?", 0) 

INSERT INTO questions(text, is_vc)
VALUES ("What separates yourself from others?", 0) 

INSERT INTO questions(text, is_vc)
VALUES ("What is your budget?", 1) 

INSERT INTO questions(text, is_vc)
VALUES ("What product are you interested in?", 1) 

