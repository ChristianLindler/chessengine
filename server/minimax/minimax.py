import time
import chess
from eval import eval_position

def move(fen, time_limit):
    start = time.time()
    def time_left():
        return time_limit - (time.time() - start)
    
    return minimax(fen, time_left, 2)


def minimax(fen, time_left, depth, my_turn=True):
    if depth <= 0 or time_left() < 0.1:
        return None, eval_position(fen)

    legal_moves = list(chess.Board(fen).legal_moves)
    
    if my_turn:
        best_move = None
        best_utility = float('-inf')
        for move in legal_moves:
            new_fen = apply_move(fen, move)
            move, move_utility = minimax(new_fen, time_left, depth - 1, False)

            if move_utility > best_utility:
                best_utility = move_utility
                best_move = move

        return best_move, best_utility

    else:
        best_move = None
        best_utility = float('inf')
        for move in legal_moves:
            new_fen = apply_move(fen, move)
            move, move_utility = minimax(new_fen, time_left, depth - 1, True)

            if move_utility < best_utility:
                best_utility = move_utility
                best_move = move

        return best_move, best_utility


def apply_move(fen, move):
    board = chess.Board(fen)
    board.push(move)
    return board.fen()


fen_example = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
print(move(fen_example, 10))