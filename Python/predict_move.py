import tensorflow as tf
import numpy as np
import chess
from encoding import encode_board, decode_move
from app import get_chessboard


# def sample_move(probs, temperature=1.0):
#     probs = np.asarray(probs).astype('float64')
#     probs = np.log(probs) / temperature
#     exp_probs = np.exp(probs)
#     probs = exp_probs / np.sum(exp_probs)
#     return np.random.choice(len(probs), p=probs)

def predict_next_move(fen):
    model = tf.keras.models.load_model('chess_model.keras')
    encoded_board = encode_board(fen)
    while True:
        predicted_move_encoded = model.predict(np.expand_dims(encoded_board, axis=0))
        # flat_index = sample_move(predicted_move_encoded[0].flatten(), temperature=0.5)
        # # Convert the flat index back to 3D shape
        # reshaped_move_encoded = np.zeros((8, 8, 2))
        # reshaped_move_encoded[np.unravel_index(flat_index, (8, 8, 2))] = 1
        uci_move = decode_move(predicted_move_encoded)
        print(uci_move)
        if is_valid_move(fen, uci_move):
            break
    return uci_move

def is_valid_move(fen, uci_move):
    board = chess.Board(fen)
    move = chess.Move.from_uci(uci_move)
    return move in board.legal_moves
# Test cases
test_cases = [
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "e2e4"),
    ("rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2", "Nf3"),
    ("rnbqkbnr/pppp1ppp/8/4p3/3P4/8/PPP2PPP/RNBQKBNR b KQkq - 0 2", "Nc6"),
    ("rnbqkbnr/pppp2pp/4p3/5p2/3P4/8/PPP2PPP/RNBQKBNR w KQkq - 0 3", "c4"),
    ("rnbqkb1r/pppppppp/5n2/8/8/5NP1/PPPPPP1P/RNBQKB1R w KQkq - 2 3", "Bg2")
]

for fen, popular_move in test_cases:
    predicted_move = predict_next_move(fen)
    print(f"Expected: {popular_move}, Predicted: {predicted_move}")
