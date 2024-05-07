-- create tables for contact and sale
CREATE TABLE contact (
    id INT NOT NULL AUTO_INCREMENT,
    first VARCHAR(256) NOT NULL,
    last VARCHAR(256) NOT NULL,
    email VARCHAR(200) NOT NULL,
    bookDate TIMESTAMP NOT NULL,
    translator VARCHAR(5) NOT NULL,
    choice VARCHAR(50) NOT NULL,
    PRIMARY KEY (id)
);

-- Create the sale table
CREATE TABLE sale (
    id INT NOT NULL AUTO_INCREMENT,
    message TEXT NOT NULL,
    active BOOLEAN DEFAULT FALSE,
    start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP DEFAULT NULL,
    PRIMARY KEY (id)
);

-- Sort id by descending order for the sale table
SELECT * FROM sale ORDER BY id DESC;

-- Add a new sale
INSERT INTO sale (message, active) VALUES ('All items are 25% off!', true);

-- Update the most recent sale to be completed
UPDATE sale SET active = FALSE ORDER BY start_time DESC LIMIT 1;

-- Get the 3 most recent sales
SELECT message, active FROM sale ORDER BY start_time DESC LIMIT 3;

