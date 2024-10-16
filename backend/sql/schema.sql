CREATE DATABASE IF NOT EXISTS chess_db;
USE chess_db;

CREATE TABLE IF NOT EXISTS game (
    game_id INT AUTO_INCREMENT PRIMARY KEY,        -- Game ID (Primary Key)
    site VARCHAR(100) DEFAULT 'Unknown',           -- Site of the game (Default: 'Unknown')
    date DATE DEFAULT CURRENT_DATE,                -- Date of the game (Default: current date)
    round INT DEFAULT NULL,                        -- Round (if applicable, Default: NULL)
    white_name VARCHAR(100) NOT NULL,              -- White player's name (required)
    black_name VARCHAR(100) NOT NULL,              -- Black player's name (required)
    result ENUM('1-0', '0-1', '1/2-1/2', '*') DEFAULT '*',  -- Default: '*' (ongoing or unknown result)
    type ENUM('Classical', 'Rapid', 'Blitz', 'Bullet') DEFAULT 'Classical', -- Default: 'Classical'
    white_elo INT DEFAULT NULL,                    -- White player's ELO rating (Default: NULL if not applicable)
    black_elo INT DEFAULT NULL,                    -- Black player's ELO rating (Default: NULL if not applicable)
    termination VARCHAR(255) DEFAULT 'Unknown',    -- How the game ended (Default: 'Unknown')
    eco VARCHAR(10) DEFAULT 'N/A',                 -- ECO code (Default: 'N/A' if not applicable)
    endtime TIME DEFAULT NULL,                     -- End time of the game (if applicable, Default: NULL)
    link VARCHAR(255) DEFAULT NULL,                -- Link to the game (if applicable, Default: NULL)
    number_of_moves INT DEFAULT 0,                 -- Default: 0 moves if not specified
    tournament_id INT DEFAULT NULL,                -- Tournament ID (if applicable, Default: NULL)

    FOREIGN KEY (white_id) REFERENCES player(player_id) ON DELETE CASCADE,  -- Cascading delete for White player
    FOREIGN KEY (black_id) REFERENCES player(player_id) ON DELETE CASCADE,  -- Cascading delete for Black player
    FOREIGN KEY (tournament_id) REFERENCES tournament(tournament_id) ON DELETE SET NULL, 
    CONSTRAINT unique_game UNIQUE (game_id)        -- Ensuring unique game IDs
);

CREATE TABLE IF NOT EXISTS move (
    game_id INT,                               -- Reference to the game (Foreign Key)
    move_number INT NOT NULL,                  -- Move number (1, 2, 3, ...)
    white_move VARCHAR(20) NOT NULL,           -- White's move (in algebraic notation)
    black_move VARCHAR(20) DEFAULT NULL,       -- Black's move (can be NULL if the game ends before black's move)
    move_time TIME DEFAULT NULL,               -- Time taken for the move (optional)

    PRIMARY KEY (game_id, move_number),

    FOREIGN KEY (game_id) REFERENCES game(game_id) 
    ON DELETE CASCADE                           -- Cascade delete to remove moves if a game is deleted
);

CREATE TABLE IF NOT EXISTS tournament (
    tournament_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique Tournament ID (Primary Key)
    name VARCHAR(100) NOT NULL,                     -- Name of the tournament
    date DATE NOT NULL,                             -- Date of the tournament
    duration INT NOT NULL,                          -- Duration of the tournament (in days)
    location VARCHAR(100),                          -- Location of the tournament
    type ENUM('Round Robin', 'Knock Out', 'Swiss System', 'Scheveningen System') DEFAULT 'Round Robin', -- Tournament type
    organizer VARCHAR(100) DEFAULT 'Unknown'       -- Organizer's name 
);

CREATE TABLE IF NOT EXISTS player (
    player_id INT AUTO_INCREMENT PRIMARY KEY,      -- Unique Player ID (Primary Key)
    name VARCHAR(100) NOT NULL,                     -- Player's name
    country VARCHAR(100) NOT NULL,                  -- Country of the player
    rating INT DEFAULT NULL,                         -- Player's rating (Default: NULL)
    email VARCHAR(100) UNIQUE,                      -- Player's email (must be unique)
    online_profile VARCHAR(255) DEFAULT NULL,       -- Links to online profiles (optional)
    date_of_birth DATE DEFAULT NULL,                -- Player's date of birth (optional)
    gender ENUM('Male', 'Female', 'Other') DEFAULT 'Other', -- Gender (optional, Default: 'Other')
);




