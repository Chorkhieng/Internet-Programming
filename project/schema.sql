-- users table
CREATE TABLE users (
    user_id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    account_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id)
);

-- posts table
CREATE TABLE posts (
    post_id INT NOT NULL AUTO_INCREMENT,
    poster_id INT,
    posted_content TEXT NOT NULL,
    like_count INT DEFAULT 0,
    post_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (post_id)
);

-- comments table
CREATE TABLE comments (
    poster_id INT,
    commenter_id INT,
    post_id INT,
    comment_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    comment_content TEXT NOT NULL
    -- allow user to delete comment(s)?
    -- commnet_id INT
);

-- create a new user
INSERT INTO users (username, password, account_name) VALUES ('chorky', 'chorky@umn', 'chorky');

-- create a new post
INSERT INTO posts (poster_id, posted_content, like_count) VALUES (1, 'I love biking in the summer time.', 5);

-- create a new comment
INSERT INTO comments (poster_id, commenter_id, post_id, comment_content) VALUES (1, 2, 1, 'I love biking too!!');

-- get 20 most recent posts by date
SELECT * FROM posts ORDER BY post_time DESC LIMIT 20;

-- get 20 most recent posts by like count
SELECT * FROM posts ORDER BY like_count DESC LIMIT 20;

-- edit post for current user
UPDATE posts SET posted_content = 'I mean biking is great!' WHERE poster_id = 1 AND post_id = 2;

-- delete post for current user
DELETE FROM posts WHERE poster_id = 1 AND post_id = 1;

-- get 10 most recent comments by date 
SELECT * FROM comments ORDER BY comment_time DESC LIMIT 10;

-- update like count
UPDATE posts SET like_count = 15 WHERE post_id = 1 AND poster_id = 1;

-- get like count for current user
SELECT like_count FROM posts WHERE poster_id = 2 AND post_id = 1;