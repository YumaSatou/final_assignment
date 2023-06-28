CREATE TABLE admin_account(
    id SERIAL PRIMARY KEY,
    name VARCHAR(64),
    hashed_password VARCHAR(64),
    salt VARCHAR(30)
);

CREATE TABLE books_list(
    id SERIAL PRIMARY KEY,
    title VARCHAR(64),
    author VARCHAR(64),
    publlisher VARCHAR(64)
);