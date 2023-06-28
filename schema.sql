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

INSERT INTO users (username, password, admin) VALUES ('admin', 'pbkdf2:sha256:260000$11Rfs8YzvmsDuVr4$f558af78b737db1de63b5866dfd5376dc958b002bd16c820c215be9dffd06cf6', 'yes');

INSERT INTO restaurants (name, description) VALUES ('Testaurant', 'A restaurant created for test purposes');
INSERT INTO restaurants (name, description) VALUES ('Kumpula Bar & Grill', 'A vegan alternative to your average 2am grill');
INSERT INTO restaurants (name, description) VALUES ('Finde Dining co.', 'For those with an expensive taste');

INSERT INTO classes (name) VALUES ('expensive');
INSERT INTO classes (name) VALUES ('cheap');
INSERT INTO classes (name) VALUES ('vegan');

INSERT INTO restaurant_classes (restaurant_id, class_id) VALUES (1,2);
INSERT INTO restaurant_classes (restaurant_id, class_id) VALUES (1,3);
INSERT INTO restaurant_classes (restaurant_id, class_id) VALUES (3,1);

INSERT INTO reviews (reviewer, stars, textreview, date, restaurant_id) VALUES ('Antti Anon', 4, 'Loved the place, but could have had more spices', '202
3-05-27 13:39:22.458804', 2);