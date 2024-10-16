-- Switch to your chess database
USE chess_db;

-- Create the Player table
CREATE TABLE Player (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    rating INT,
    country VARCHAR(100),
    date_joined DATE
);

-- Create the Tournament table
CREATE TABLE Tournament (
    tournament_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    start_date DATE,
    end_date DATE
);

-- Create the Game table
CREATE TABLE Game (
    game_id INT AUTO_INCREMENT PRIMARY KEY,
    white_player_id INT,
    black_player_id INT,
    result VARCHAR(10),
    date_played DATE,
    time_control VARCHAR(50),
    tournament_id INT,
    FOREIGN KEY (white_player_id) REFERENCES Player(player_id),
    FOREIGN KEY (black_player_id) REFERENCES Player(player_id),
    FOREIGN KEY (tournament_id) REFERENCES Tournament(tournament_id)
);

-- Create the Move table
CREATE TABLE Move (
    move_id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT,
    move_number INT,
    move VARCHAR(10),
    player_id INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (game_id) REFERENCES Game(game_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id)
);

-- Create the Administrator table
CREATE TABLE Administrator (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    email VARCHAR(255),
    full_name VARCHAR(255)
);

-- (Optional) Create the Opening table
CREATE TABLE Opening (
    opening_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    eco_code VARCHAR(10),
    common_moves TEXT
);

-- Create the GameOpening linking table (optional)
CREATE TABLE GameOpening (
    game_id INT,
    opening_id INT,
    PRIMARY KEY (game_id, opening_id),
    FOREIGN KEY (game_id) REFERENCES Game(game_id),
    FOREIGN KEY (opening_id) REFERENCES Opening(opening_id)
);
