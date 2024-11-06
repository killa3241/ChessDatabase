import re

class ParsedGame:
    def __init__(self):
        self.players = {"white": {}, "black": {}}
        self.tournament = {}
        self.game = {}
        self.moves = []

def parse_pgn(pgn_content):
    print(pgn_content)
    games = []
    game_strings = pgn_content.strip().split("\n\n\n")  # Split games by double newlines

    for game_string in game_strings:
        if '[Event' not in game_string:
            continue

        parts = game_string.split("\n\n", 1)
        if len(parts) < 2:
            continue

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
        parsed_game.game["white_elo"] = headers_dict.get("WhiteElo", None)
        parsed_game.game["black_elo"] = headers_dict.get("BlackElo", None)
        parsed_game.game["site"] = parsed_game.tournament["site"]
        parsed_game.game["result"] = headers_dict.get("Result", "*")
        parsed_game.game["termination"] = headers_dict.get("Termination", "Unknown")
        parsed_game.game["eco"] = headers_dict.get("ECO", "N/A")
        parsed_game.game["time_control"] = headers_dict.get("TimeControl", "Classical")
        parsed_game.game["link"] = headers_dict.get("Link", None)

        # Parse moves
        moves = re.findall(r'\d+\.\s+(\S+)\s+(\S+)?', moves_text)
        for move_number, (white_move, black_move) in enumerate(moves, start=1):
            parsed_game.moves.append({
                "move_number": move_number,
                "white_move": white_move.strip(),
                "black_move": black_move.strip() if black_move else None
            })

        games.append(parsed_game)

    return games
