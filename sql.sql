CREATE DATABASE IF NOT EXISTS cinescope;
USE cinescope;

CREATE TABLE movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    genre VARCHAR(100),
    year INT,
    rating FLOAT
);

INSERT INTO movies (title, genre, year, rating) VALUES
('Inception', 'Sci-Fi', 2010, 8.8),
('The Dark Knight', 'Action', 2008, 9.0),
('Interstellar', 'Sci-Fi', 2014, 8.6),
('Parasite', 'Thriller', 2019, 8.6),
('The Godfather', 'Crime', 1972, 9.2),
('Pulp Fiction', 'Crime', 1994, 8.9),
('The Shawshank Redemption', 'Drama', 1994, 9.3),
('Fight Club', 'Drama', 1999, 8.8),
('The Matrix', 'Sci-Fi', 1999, 8.7),
('Forrest Gump', 'Drama', 1994, 8.8);
