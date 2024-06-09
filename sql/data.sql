PRAGMA foreign_keys = ON;

INSERT INTO users(username, name, password, filename, is_vc, points, industry, summary)
VALUES ('aaa', 'Company A', 'password', 'logo_1.jpg', 0, 0, 'Tech', 'wow');

INSERT INTO users(username, name, password, filename, is_vc, points, industry, summary)
VALUES ('bbb', 'Company B', 'password', 'logo_2.jpg', 0, 0, 'Consulting', 'wow');

INSERT INTO users(username, name, password, filename, is_vc, points, industry, summary)
VALUES ('ccc', 'Company C', 'password', 'logo_3.jpg', 0, 0, 'Transportation', 'wow');

INSERT INTO users(username, name, password, filename, is_vc, points, industry, summary)
VALUES ('zzz', 'Investor Z', 'password', 'logo_3.jpg', 1, 0, 'Transportation', 'wow');

INSERT INTO users(username, name, password, filename, is_vc, points, industry, summary)
VALUES ('ychengpoon', 'poon poon', 'password', '', 1, 0, 'Tech', 'Im great');

INSERT INTO questions(question, is_vc)
VALUES ('What is your preferred investment amount?', 1); 

INSERT INTO questions(question, is_vc)
VALUES ('What are your preferred industries?', 1); 

INSERT INTO questions(question, is_vc)
VALUES ('What is your preferred revenue size?', 1); 

INSERT INTO questions(question, is_vc)
VALUES ('What are the aspects of the company you wish to know the most about?', 1); 

INSERT INTO questions(question, is_vc)
VALUES ('List of keywords you are looking from a company.', 1); 

INSERT INTO questions(question, is_vc)
VALUES ('What product are you interested in?', 1);

INSERT INTO questions(question, is_vc)
VALUES ('Tell me more about yourself', 0);

INSERT INTO questions(question, is_vc)
VALUES ('What services or products are you selling?', 0);

INSERT INTO questions(question, is_vc)
VALUES ('What do you envision your company to look like in the future?', 0);

INSERT INTO questions(question, is_vc)
VALUES ('How can your company tackle its goals in an environmentally-sustainable manner?', 0);

INSERT INTO questions(question, is_vc)
VALUES ('What kind of employees are you looking for?', 0); 

INSERT INTO questions(question, is_vc)
VALUES ('How extensive is your company''s reach in terms of its influence?', 0);

INSERT INTO questions(question, is_vc)
VALUES ('If your company can only solve one problem, what would it be?', 0);

INSERT INTO questions(question, is_vc)
VALUES ('How involved do you think the government should be in corporate business & regulations?', 0); 

INSERT INTO questions(question, is_vc)
VALUES ('If your were to face a financial decline, what would be your approach in mitigating that?', 0);

INSERT INTO questions(question, is_vc)
VALUES ('How much do you think marketing actually contributes to the growth of your product?', 0); 

INSERT INTO answers(question_id, answer, username)
VALUES (1, '15 billion USD', 'ychengpoon');

INSERT INTO answers(question_id, answer, username)
VALUES (2, 'AI', 'ychengpoon');

INSERT INTO answers(question_id, answer, username)
VALUES (3, '2 billion USD', 'ychengpoon');

INSERT INTO answers(question_id, answer, username)
VALUES (4, 'Company Vision, Company''s Plan for the Next 12 Month, Company''s Competitive Advantage', 'ychengpoon');

INSERT INTO answers(question_id, answer, username)
VALUES (5, 'Budget, AI Solution, Valuation', 'ychengpoon');

