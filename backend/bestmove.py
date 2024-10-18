import chess
import chess.engine

def get_best_move(fen_position):
    # Connect to the Stockfish engine
    with chess.engine.SimpleEngine.popen_uci(r"E:\Akshay\temp\stockfish-windows-x86-64\stockfish\stockfish-windows-x86-64.exe") as engine:
        # Set up the position
        board = chess.Board(fen_position)
        
        # Analyze the position for 1 second (or set a custom time)
        result = engine.analyse(board, chess.engine.Limit(time=1.0))
        
        # Get the best move and evaluation score
        best_move = result['pv'][0]
        evaluation = result['score'].relative.score()
        
        return best_move, evaluation

# Example usage
fen = "r1bqkb1r/ppp2ppp/2n2n2/3pp3/3PP3/2N2N2/PPP2PPP/R1BQKB1R w KQkq - 0 1"  # Starting position
move, score = get_best_move(fen)
print(f"Best move: {move}, Evaluation: {score}")
