CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    admin TEXT
);

CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT
);

CREATE TABLE classes (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE restaurant_classes (
    id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurants ON DELETE CASCADE,
    class_id INTEGER REFERENCES classes ON DELETE CASCADE
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    reviewer TEXT,
    stars INTEGER,
    textreview TEXT,
    date TIMESTAMP,
    restaurant_id INTEGER REFERENCES restaurants ON DELETE CASCADE
);