CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL
);

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    likes INTEGER DEFAULT 0
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    text VARCHAR(200) NOT NULL,
    item_id INTEGER REFERENCES items(id) ON DELETE CASCADE
);


--Query
-- SELECT * FROM users
-- WHERE count(username) < 2
