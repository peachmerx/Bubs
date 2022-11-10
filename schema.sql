DROP TABLE IF EXISTS toys;
CREATE TABLE toys (
    id SERIAL PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    name VARCHAR(50) NOT NULL,
    price INTEGER NOT NULL,
    image_url TEXT
);

DROP TABLE IF EXISTS clothes;
CREATE TABLE clothes (
    id SERIAL PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    name VARCHAR(50) NOT NULL,
    price INTEGER NOT NULL,
    image_url TEXT
);

DROP TABLE IF EXISTS books;
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    name VARCHAR(50) NOT NULL,
    price INTEGER NOT NULL,
    image_url TEXT
);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT,
    password_hash TEXT,
    verified BOOLEAN
);