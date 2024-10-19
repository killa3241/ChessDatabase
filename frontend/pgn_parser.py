def parse_pgn(pgn_content):
    """Parses the provided PGN content and extracts game details and moves."""
    # Split the PGN content into lines and filter out comments and empty lines
    lines = pgn_content.splitlines()
    moves_line = []
    
    # Read moves from the PGN content
    for line in lines:
        line = line.strip()
        if line and not line.startswith("["):  # Exclude headers and comments
            moves_line.append(line)

    # Join the moves line into a single string
    moves_string = ' '.join(moves_line).strip()

    # Split the moves based on spaces
    tokens = moves_string.split()

    # Prepare game details and moves
    game_data = {
        'white_name': 'Unknown',
        'black_name': 'Unknown',
        'result': '*'
    }

    moves = []
    
    # Iterate over the tokens to extract moves
    for i, token in enumerate(tokens):
        if token.endswith('.'):  # Move number
            continue
        
        # Determine if the move is for White or Black
        if i % 2 == 0:  # White's turn (even index)
            moves.append({'white_move': token, 'black_move': None})
        else:  # Black's turn (odd index)
            moves[-1]['black_move'] = token

    return game_data, moves
