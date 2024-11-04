import re

# Define a class to represent the parsed PGN game data
class ParsedGame:
    def __init__(self):
        self.players = {"white": {}, "black": {}}
        self.tournament = {}
        self.game = {}
        self.moves = []

def parse_pgn(file_path):
    games = []

    with open(file_path) as pgn_file:
        raw_content = pgn_file.read()
        game_strings = raw_content.strip().split("\n\n\n")  # Split games by double newlines with spacing

        for game_string in game_strings:
            if '[Event' not in game_string:
                continue  # Skip entries without headers

            parts = game_string.split("\n\n", 1)
            if len(parts) < 2:
                continue  # Skip if no moves section found

            header, moves_text = parts
            parsed_game = ParsedGame()

            # Extract headers
            headers = re.findall(r'\[(\w+)\s+"([^"]+)"\]', header)
            headers_dict = {key: value for key, value in headers}

            parsed_game.players["white"]["name"] = headers_dict.get("White", "Unknown")
            parsed_game.players["black"]["name"] = headers_dict.get("Black", "Unknown")
            parsed_game.tournament["name"] = headers_dict.get("Event", "Unknown")
            parsed_game.tournament["site"] = headers_dict.get("Site", "Unknown")
            parsed_game.tournament["date"] = headers_dict.get("Date", "0000.00.00")
            parsed_game.game["white_name"] = parsed_game.players["white"]["name"]
            parsed_game.game["black_name"] = parsed_game.players["black"]["name"]
            parsed_game.game["site"] = parsed_game.tournament["site"]
            parsed_game.game["result"] = headers_dict.get("Result", "*")
            parsed_game.game["termination"] = headers_dict.get("Termination", "Unknown")
            parsed_game.game["eco"] = headers_dict.get("ECO", "N/A")
            parsed_game.game["time_control"] = headers_dict.get("TimeControl", "Unknown")

            # Parse moves
            moves = re.findall(r'\d+\.\s+(\S+)\s+(\S+)?', moves_text)
            for move_number, (white_move, black_move) in enumerate(moves, start=1):
                # Assign moves directly
                parsed_game.moves.append({
                    "move_number": move_number,
                    "white_move": white_move.strip(),
                    "black_move": black_move.strip() if black_move else None
                })

            games.append(parsed_game)

    return games

# Test the parser with a sample PGN file
file_path = "F:\\PROGRAMMING RELATED\\Downloads\\AtishayJ210_vs_mrman69429_2024.10.29.pgn"
parsed_games = parse_pgn(file_path)

# Print the parsed data for inspection
for game in parsed_games:
    print("Players:", game.players)
    print("Tournament:", game.tournament)
    print("Game:", game.game)
    print("Moves:", game.moves)
    print("\n" + "-"*50 + "\n")
