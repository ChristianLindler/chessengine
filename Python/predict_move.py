from tensorflow.keras.models import load_model
import numpy as np
from encoding import encode_board, decode_move
from app import get_chessboard

def predict_next_move(fen):
    model = load_model('chess_model.h5')
    board = get_chessboard()
    encoded_board = encode_board(board)
    
    predicted_move_encoded = model.predict(np.expand_dims(encoded_board, axis=0))
    
    uci_move = decode_move(predicted_move_encoded[0])
    
    return uci_move

# test
current_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"  # Starting position
predicted_move = predict_next_move(current_fen)
print(predicted_move)