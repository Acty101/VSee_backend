PRAGMA foreign_keys = ON;

CREATE TABLE users(
  username VARCHAR(20) NOT NULL,
  name VARCHAR(40) NOT NULL,
  password VARCHAR (256) NOT NULL,
  filename VARCHAR(64) NOT NULL,
  is_vc BIT NOT NULL, 
  points INTEGER NOT NULL, 
  industry VARCHAR(64) NOT NULL,
  summary VARCHAR(64) NOT NULL,
  PRIMARY KEY(username)
);

CREATE TABLE questions(
  question_id INTEGER PRIMARY KEY AUTOINCREMENT,
  question VARCHAR(256) NOT NULL,
  is_vc BIT NOT NULL
);

CREATE TABLE answers(
    answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    answer VARCHAR(256) NOT NULL,
    username VARCHAR(20) NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);

CREATE TABLE bot_summary(
    summary_id INTEGER PRIMARY KEY AUTOINCREMENT,
    startup_username VARCHAR(20) NOT NULL,
    vc_username VARCHAR(20) NOT NULL,
    summary VARCHAR(1000000) NOT NULL,
    filename VARCHAR(50) NOT NULL
);

