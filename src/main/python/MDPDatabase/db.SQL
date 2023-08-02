DROP TABLE IF EXISTS Password;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS UserSecurity;

CREATE TABLE Password (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    site TEXT,
    identifier TEXT,
    password TEXT,
    icon TEXT,
    FOREIGN KEY(user) REFERENCES User(username)
);

CREATE TABLE User (
    username TEXT PRIMARY KEY UNIQUE ,
    times_connected INTEGER,
    serial_number INTEGER UNIQUE
);

CREATE TABLE UserSecurity (
    user TEXT PRIMARY KEY,
    hashed_password TEXT,
    hashed_answer TEXT,
    encrypted_password TEXT,
    encrypted_question TEXT,
    salt BINARY,
    FOREIGN KEY(user) REFERENCES User(username)
);