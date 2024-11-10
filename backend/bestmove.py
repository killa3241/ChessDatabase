import chess
import chess.engine

STOCKFISH_PATH=r"E:\Akshay\temp\stockfish-windows-x86-64\stockfish\stockfish-windows-x86-64.exe"
def get_best_move(fen_position):
    # Connect to the Stockfish engine
    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        # Set up the position
        board = chess.Board(fen_position)
        
        # Analyze the position for 1 second (or set a custom time)
        result = engine.analyse(board, chess.engine.Limit(time=1.0))
        
        # Get the best move and evaluation score
        best_move = result['pv'][0]
        evaluation = result['score'].relative.score()
        
        return best_move, evaluation

# Example usage
#fen = "r1bqkb1r/ppp2ppp/2n2n2/3pp3/3PP3/2N2N2/PPP2PPP/R1BQKB1R w KQkq - 0 1"  # Starting position
#move, score = get_best_move(fen)
#print(f"Best move: {move}, Evaluation: {score}")
fen_list = [
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",  # Starting Position
    "rnbqkbnr/ppppp1pp/8/8/4P3/8/PPP1P1PP/RNBQKBNR b KQkq - 1 1",  # King's Pawn Opening
    "rnbqkbnr/ppppp1pp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1",  # Queen's Gambit Declined
    "rnbqkbnr/ppppp1pp/8/3P4/3P4/8/PPP1P1PP/RNBQKBNR b KQkq - 0 1",  # Italian Game
    "rnbqkbnr/ppppp1pp/8/8/8/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1",  # Sicilian Defense
    "rnbqkbnr/ppppp1pp/8/8/8/3P4/PPP1PPPP/RNBQKBNR w KQkq - 1 1",  # French Defense
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",  # English Opening
    "rnbqkbnr/ppppp1pp/8/8/4P3/3P4/PPP1PPPP/RNBQKBNR b KQkq - 0 1",  # Scotch Game
    "rnbqkbnr/pppppppp/8/8/8/2P5/PPP1P1PP/RNBQKBNR w KQkq - 1 1",  # King's Indian Defense
    "rnbqkbnr/pppppppp/8/8/8/2P5/PPP1P1PP/RNBQKBNR w KQkq - 0 1",  # Nimzo-Indian Defense
    "rnbqkbnr/ppp2ppp/8/3P4/8/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1",  # Caro-Kann Defense
    "rnbqkbnr/ppp1pppp/8/3p4/8/8/PPP1PPPP/RNBQKBNR w KQkq - 1 1",  # Petrov Defense
    "rnbqkbnr/ppppp1pp/8/8/4P3/3P4/PPP1P1PP/RNBQKBNR b KQkq - 0 1",  # Giuoco Piano
    "rnbqkbnr/pppppppp/8/8/2B5/8/PPP1PPPP/RNBQK1NR b KQkq - 1 1",  # Ruy Lopez
    "rnbqkbnr/pp1ppppp/5n2/8/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 1 1",  # Sicilian Dragon
    "rnbqkbnr/pppppppp/8/8/8/2P5/PPP1P1PP/RNBQKBNR w KQkq - 0 1",  # King's Gambit
    "rnbqkbnr/pp1ppppp/2n5/3P4/8/8/PPP1PPPP/RNBQKBNR w KQkq - 1 1",  # Queen's Indian Defense
    "rnbqkbnr/pp1ppppp/8/3P4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 1 1",  # Sicilian Najdorf
    "rnbqkbnr/pp1ppppp/8/8/2p5/8/PPP1PPPP/RNBQKBNR w KQkq - 1 1"   # Alekhine Defense
]





for i in fen_list:
    move, score = get_best_move(i)
    print(f"Best move: {move}, Evaluation: {score}")

