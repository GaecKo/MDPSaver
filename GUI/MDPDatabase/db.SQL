DROP TABLE IF EXISTS Password;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS UserSecurity;

CREATE TABLE Password (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  site TEXT,
  username TEXT,
  password TEXT
);

CREATE TABLE User (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT,
  times_connected INTEGER,
  serial_number INTEGER UNIQUE
);

CREATE TABLE UserSecurity (
  username TEXT PRIMARY KEY,
  hashed_password TEXT,
  hashed_answer TEXT,
  encrypted_password TEXT,
  encrypted_question TEXT,
  salt BINARY,
  FOREIGN KEY(username) REFERENCES User(username)
);