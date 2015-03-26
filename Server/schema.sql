CREATE TABLE users (
	id int PRIMARY KEY,
	user_fb_id int NOT NULL);
	
CREATE TABLE spaces (
	user_id INT NOT NULL,
	image_id INT NOT NULL,
	space BOOLEAN NOT NULL);
	
ALTER TABLE spaces ADD FOREIGN KEY (user_id) REFERENCES users(id); 
