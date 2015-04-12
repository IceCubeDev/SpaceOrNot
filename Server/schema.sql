CREATE TABLE pictures (
     id INT PRIMARY KEY,
     path TEXT NOT NULL
);

CREATE TABLE users (
     id SERIAL PRIMARY KEY,
     fb_id TEXT NOT NULL,
     real_name TEXT
);

CREATE TABLE spaces (
     pic_id INT NOT NULL,
     user_id INT NOT NULL,
     space BOOLEAN
);
