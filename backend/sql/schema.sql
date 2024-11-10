CREATE DATABASE IF NOT EXISTS chess_db;
USE chess_db;

CREATE TABLE IF NOT EXISTS player (
    player_id VARCHAR(15) PRIMARY KEY,      -- Unique Player ID (Primary Key)
    name VARCHAR(100) DEFAULT NULL,                     -- Player's name
    country VARCHAR(100) DEFAULT NULL,                  -- Country of the player
    rating INT DEFAULT NULL,                         -- Player's rating (Default: NULL)
    email VARCHAR(100) UNIQUE,                      -- Player's email (must be unique)
    password VARCHAR(255) DEFAULT NULL,                 -- Hashed password (stored securely)
    online_profile VARCHAR(255) DEFAULT NULL,       -- Links to online profiles
    date_of_birth DATE DEFAULT NULL,                -- Player's date of birth
    gender ENUM('Male', 'Female', 'Other') DEFAULT NULL -- Gender
);

CREATE TABLE IF NOT EXISTS profile_status (
    player_id VARCHAR(15) PRIMARY KEY,
    is_profile_complete BOOLEAN DEFAULT 0,
    FOREIGN KEY (player_id) REFERENCES player(player_id) ON DELETE CASCADE
);

DELIMITER //
CREATE TRIGGER after_player_insert
AFTER INSERT ON player
FOR EACH ROW
BEGIN
    DECLARE profile_complete BOOLEAN;
    SET profile_complete = 
        (NEW.name IS NOT NULL AND 
         NEW.country IS NOT NULL AND 
         NEW.rating IS NOT NULL AND 
         NEW.date_of_birth IS NOT NULL AND 
         NEW.gender IS NOT NULL);
    INSERT INTO profile_status (player_id, is_profile_complete)
    VALUES (NEW.player_id, profile_complete)
    ON DUPLICATE KEY UPDATE is_profile_complete = profile_complete;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER after_player_update
AFTER UPDATE ON player
FOR EACH ROW
BEGIN
    DECLARE profile_complete BOOLEAN;

    -- Check if all required fields are filled
    SET profile_complete = 
        (NEW.name IS NOT NULL AND 
         NEW.country IS NOT NULL AND 
         NEW.rating IS NOT NULL AND 
         NEW.date_of_birth IS NOT NULL AND 
         NEW.gender IS NOT NULL);

    -- Update the profile_status table if the player already exists
    UPDATE profile_status
    SET is_profile_complete = profile_complete
    WHERE player_id = NEW.player_id;
END //
DELIMITER ;

CREATE TABLE IF NOT EXISTS tournament (
    tournament_id VARCHAR(6) PRIMARY KEY,  -- Unique Tournament ID (Primary Key)
    name VARCHAR(100) NOT NULL,                     -- Name of the tournament
    date DATE NOT NULL,                             -- Date of the tournament
    duration INT NOT NULL,                          -- Duration of the tournament (in days)
    location VARCHAR(100),                          -- Location of the tournament
    type ENUM('Round Robin', 'Knock Out', 'Swiss System', 'Scheveningen System') DEFAULT 'Round Robin', -- Tournament type
    organizer VARCHAR(100) DEFAULT 'Unknown'       -- Organizer's name 
);

CREATE TABLE IF NOT EXISTS game (
    game_id VARCHAR(8) PRIMARY KEY,        -- Game ID (Primary Key)
    site VARCHAR(100) DEFAULT 'Unknown',           -- Site of the game (Default: 'Unknown')
    date DATE DEFAULT NULL,                -- Date of the game (Default: current date)
    round INT DEFAULT NULL,                        -- Round (if applicable, Default: NULL)
    white_name VARCHAR(100) NOT NULL,              -- White player's name (required)
    white_id VARCHAR(15) NOT NULL,                         -- Foreign key usage
    black_name VARCHAR(100) NOT NULL,              -- Black player's name (required)
    black_id VARCHAR(15) NOT NULL,                         -- Foreign key usage
    result ENUM('1-0', '0-1', '1/2-1/2', '*') DEFAULT '*',  -- Default: '*' (ongoing or unknown result)
    type VARCHAR(20), 
    white_elo INT DEFAULT NULL,                    -- White player's ELO rating (Default: NULL if not applicable)
    black_elo INT DEFAULT NULL,                    -- Black player's ELO rating (Default: NULL if not applicable)
    termination VARCHAR(255) DEFAULT 'Unknown',    -- How the game ended (Default: 'Unknown')
    eco VARCHAR(10) DEFAULT 'N/A',                 -- ECO code (Default: 'N/A' if not applicable)
    endtime TIME DEFAULT NULL,                     -- End time of the game (if applicable, Default: NULL)
    link VARCHAR(255) DEFAULT NULL,                -- Link to the game (if applicable, Default: NULL)
    number_of_moves INT DEFAULT 0,                 -- Default: 0 moves if not specified
    tournament_id VARCHAR(6) DEFAULT NULL,                -- Tournament ID (if applicable, Default: NULL)

    FOREIGN KEY (white_id) REFERENCES player(player_id) ON DELETE CASCADE,  -- Cascading delete for White player
    FOREIGN KEY (black_id) REFERENCES player(player_id) ON DELETE CASCADE,  -- Cascading delete for Black player
    FOREIGN KEY (tournament_id) REFERENCES tournament(tournament_id) ON DELETE SET NULL, 
    CONSTRAINT unique_game UNIQUE (game_id)        -- Ensuring unique game IDs
);

DELIMITER //
CREATE TRIGGER update_player_rating_after_game
AFTER INSERT ON game
FOR EACH ROW
BEGIN
    IF NEW.white_elo IS NOT NULL THEN
        UPDATE player
        SET rating = NEW.white_elo
        WHERE player_id = NEW.white_id;
    END IF;
    IF NEW.black_elo IS NOT NULL THEN
        UPDATE player
        SET rating = NEW.black_elo
        WHERE player_id = NEW.black_id;
    END IF;
END //
DELIMITER ;

CREATE TABLE IF NOT EXISTS move (
    game_id VARCHAR(8),                               -- Reference to the game (Foreign Key)
    move_number INT NOT NULL,                  -- Move number (1, 2, 3, ...)
    white_move VARCHAR(20) NOT NULL,           -- White's move (in algebraic notation)
    black_move VARCHAR(20) DEFAULT NULL,       -- Black's move (can be NULL if the game ends before black's move)
    move_time TIME DEFAULT NULL,               -- Time taken for the move (optional)

    PRIMARY KEY (game_id, move_number),
    FOREIGN KEY (game_id) REFERENCES game(game_id) 
    ON DELETE CASCADE                           -- Cascade delete to remove moves if a game is deleted
);

DELIMITER //

CREATE PROCEDURE get_player_statistics(IN p_player_id VARCHAR(15))
BEGIN
    SELECT 
        p.player_id,
        p.name,
        COUNT(DISTINCT g.game_id) AS total_games,
        SUM(CASE 
            WHEN (g.white_id = p.player_id AND g.result = '1-0') 
                OR (g.black_id = p.player_id AND g.result = '0-1') 
            THEN 1 ELSE 0 END) AS wins,
        SUM(CASE 
            WHEN g.result = '1/2-1/2' THEN 1 ELSE 0 END) AS draws,
        ROUND(
            100.0 * SUM(CASE 
                WHEN (g.white_id = p.player_id AND g.result = '1-0') 
                    OR (g.black_id = p.player_id AND g.result = '0-1') 
                THEN 1 ELSE 0 END) / NULLIF(COUNT(DISTINCT g.game_id), 0), 2) AS win_rate,
        ROUND(
            AVG(CASE WHEN g.white_id = p.player_id THEN g.black_elo ELSE g.white_elo END), 
        2) AS avg_opponent_elo,
        MAX(CASE WHEN g.white_id = p.player_id THEN g.black_elo ELSE g.white_elo END) AS highest_opponent_elo,
        (
            SELECT type 
            FROM game g2
            WHERE (g2.white_id = p.player_id OR g2.black_id = p.player_id)
            GROUP BY type
            ORDER BY COUNT(*) DESC
            LIMIT 1
        ) AS preferred_time_control,
        (
            SELECT white_move
            FROM (
                SELECT m.white_move, COUNT(*) as move_count
                FROM game g3
                JOIN move m ON g3.game_id = m.game_id
                WHERE g3.white_id = p.player_id AND m.move_number = 1
                GROUP BY m.white_move
                ORDER BY move_count DESC
                LIMIT 1
            ) white_moves
        ) AS favorite_white_opening,
        (
            SELECT black_move
            FROM (
                SELECT m.black_move, COUNT(*) as move_count
                FROM game g4
                JOIN move m ON g4.game_id = m.game_id
                WHERE g4.black_id = p.player_id AND m.move_number = 1
                GROUP BY m.black_move
                ORDER BY move_count DESC
                LIMIT 1
            ) black_moves
        ) AS favorite_black_opening
    FROM player p
    LEFT JOIN game g ON p.player_id = g.white_id OR p.player_id = g.black_id
    WHERE p.player_id = p_player_id OR p_player_id IS NULL
    GROUP BY p.player_id, p.name
    ORDER BY total_games DESC;
END//

DELIMITER ;

CREATE TABLE IF NOT EXISTS best_moves (
    fen VARCHAR(255) PRIMARY KEY,  
    best_move VARCHAR(10) NOT NULL,
    evaluation FLOAT NOT NULL DEFAULT 0 
);



