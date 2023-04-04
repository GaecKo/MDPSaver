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
  userId INTEGER,
  hashed_password TEXT,
  hashed_answer TEXT,
  encrypted_password TEXT,
  encrypted_question TEXT,
  FOREIGN KEY(userId) REFERENCES User(id)
);