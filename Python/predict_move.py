from tensorflow import keras
import numpy as np
import chess
from encoding import encode_board, decode_move
from app import get_chessboard

def predict_next_move(fen):
    model = keras.models.load_model('chess_model.h5')
    board = get_chessboard()
    encoded_board = encode_board(board)
    while True:
        predicted_move_encoded = model.predict(np.expand_dims(encoded_board, axis=0))
        uci_move = decode_move(predicted_move_encoded[0])
        if is_valid_move(board, uci_move):
            break
    return uci_move

def is_valid_move(fen, uci_move):
    board = chess.Board(fen)
    move = chess.Move.from_uci(uci_move)
    return move in board.legal_moves
# test
current_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"  # Starting position
predicted_move = predict_next_move(current_fen)
print(predicted_move)