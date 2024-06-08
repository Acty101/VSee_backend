PRAGMA foreign_keys = ON;

INSERT INTO users(username, name, password, filename, is_vc, points, industry)
VALUES ('aaa', 'Company A', 'password', 'startup_1.jpg', 0, 0, 'Tech');

INSERT INTO users(username, name, password, filename, is_vc, points, industry)
VALUES ('bbb', 'Company B', 'password', 'startup_2.jpg', 0, 0, 'Consulting');

INSERT INTO users(username, name, password, filename, is_vc, points, industry)
VALUES ('ccc', 'Company C', 'password', 'startup_3.jpg', 0, 0, 'Transportation');

INSERT INTO users(username, name, password, filename, is_vc, points, industry)
VALUES ('zzz', 'Investor Z', 'password', 'vc_1.jpg', 1, 0, 'Transportation');


INSERT INTO questions(text) 
VALUES ('Question 1');

INSERT INTO questions(text) 
VALUES ('Question 2');

INSERT INTO questions(text) 
VALUES ('Question 3');

INSERT INTO questions(text) 
VALUES ('Question 4');

INSERT INTO questions(text) 
VALUES ('Question 5');

INSERT INTO answers(question_id, text, username)
VALUES (1, 'Answer 1', 'aaa');

INSERT INTO answers(question_id, text, username)
VALUES (2, 'Answer 2', 'aaa');

INSERT INTO answers(question_id, text, username)
VALUES (3, 'Answer 3', 'aaa');

INSERT INTO answers(question_id, text, username)
VALUES (4, 'Answer 4', 'aaa');

INSERT INTO answers(question_id, text, username)
VALUES (5, 'Answer 5', 'aaa');

INSERT INTO answers(question_id, text, username)
VALUES (1, 'Answer 1', 'bbb');

INSERT INTO answers(question_id, text, username)
VALUES (2, 'Answer 2', 'bbb');

INSERT INTO answers(question_id, text, username)
VALUES (3, 'Answer 3', 'bbb');

INSERT INTO answers(question_id, text, username)
VALUES (4, 'Answer 4', 'bbb');

INSERT INTO answers(question_id, text, username)
VALUES (5, 'Answer 5', 'bbb');

INSERT INTO answers(question_id, text, username)
VALUES (1, 'Answer 1', 'ccc');

INSERT INTO answers(question_id, text, username)
VALUES (2, 'Answer 2', 'ccc');

INSERT INTO answers(question_id, text, username)
VALUES (3, 'Answer 3', 'ccc');

INSERT INTO answers(question_id, text, username)
VALUES (4, 'Answer 4', 'ccc');

INSERT INTO answers(question_id, text, username)
VALUES (5, 'Answer 5', 'ccc');

INSERT INTO bot_summary(startup_username, vc_username, text)
VALUES ('aaa', 'zzz', 'Summary aaa for zzz');

INSERT INTO bot_summary(startup_username, vc_username, text)
VALUES ('bbb', 'zzz', 'Summary bbb for zzz');

INSERT INTO bot_summary(startup_username, vc_username, text)
VALUES ('ccc', 'zzz', 'Summary ccc for zzz');
