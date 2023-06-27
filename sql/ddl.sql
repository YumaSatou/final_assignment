CREATE TABLE admin_account(
    id SERIAL PRIMARY KEY,
    name VARCHAR(64),
    mail VARCHAR(100) unique,
    hashed_password VARCHAR(64),
    salt VARCHAR(30)
);