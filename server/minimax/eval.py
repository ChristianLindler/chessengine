def eval_position(fen):
    piece_values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0,
                    'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': 0}

    board_state, turn, castling, en_passant, halfmove, fullmove = fen.split()
    material_score = sum(piece_values.get(piece, 0) for piece in board_state)

    return material_score


fen_example = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
evaluation_score = eval_position(fen_example)
print(f"Evaluation Score: {evaluation_score}")
