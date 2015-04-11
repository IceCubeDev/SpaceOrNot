CREATE TABLE pictures (
     id INT PRIMARY KEY,
     path STRING NOT NULL,
);

CREATE TABLE users (
     id INT PRIMARY KEY,
     fb_id STRING NOT NULL
);

CREATE TABLE spaces (
     pic_id INT NOT NULL,
     user_id INT NOT NULL,
     space BOOLEAN
);
