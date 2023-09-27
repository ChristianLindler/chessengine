import tensorflow as tf
import numpy as np
import chess
from encoding import encode_board, decode_move
from app import get_chessboard



# def predict_next_move(fen):
#     # Load the piece selection model
#     piece_selection_model = tf.keras.models.load_model('piece_selection_model.keras', safe_mode=False)
#     encoded_board = encode_board(fen)
    
#     # Predict the piece type
#     piece_probs = piece_selection_model.predict(np.expand_dims(encoded_board, axis=0))
#     predicted_piece_type = np.argmax(piece_probs)
    
#     # Load the corresponding piece model based on the predicted piece type
#     piece_model = tf.keras.models.load_model(f'chess_model_for_piece_{predicted_piece_type}.keras', safe_mode=False)
    
#     # Predict the move using the piece model
#     while True:
#         predicted_move_encoded = piece_model.predict(np.expand_dims(encoded_board, axis=0))
#         uci_move = decode_move(predicted_move_encoded)
        
#         # Check if we should use the full UCI format or just the piece type + destination
#         end_square = chess.SQUARE_NAMES.index(uci_move[2:])
#         full_uci_required = should_use_full_uci(fen, predicted_piece_type, end_square)
        
#         if full_uci_required:
#             # Use the full UCI format
#             print(uci_move)
#             if is_valid_move(fen, uci_move):
#                 break
#         else:
#             # Use the piece type + destination format
#             piece_symbol = ['P', 'N', 'B', 'R', 'Q', 'K'][predicted_piece_type]
#             short_move = piece_symbol + uci_move[2:]
#             print(short_move)
#             if is_valid_move(fen, short_move):
#                 uci_move = short_move
#                 break

#     return uci_move

def predict_next_move(fen):
    # Load the piece selection model
    piece_selection_model = tf.keras.models.load_model('piece_selection_model.keras', compile=False, safe_mode=False)
    encoded_board = encode_board(fen)
    
    # Predict the piece type
    piece_probs = piece_selection_model.predict(np.expand_dims(encoded_board, axis=0))[0]
    
    # Load all piece models
    piece_models = {i: tf.keras.models.load_model(f'chess_model_for_piece_{i}.keras', compile=False, safe_mode=False) for i in range(6)}
    
    # Predict the move for each piece and combine predictions 
    # combined_probs = np.zeros((8, 8, 8, 8, 6))  # 8x8 start position, 8x8 end position, 6 piece types
    # for piece_type, piece_model in piece_models.items():
    #     move_probs = piece_model.predict(np.expand_dims(encoded_board, axis=0))[0]
    
    #     move_probs *= is_legal_move(fen, piece_type)
        
    #     for start_rank in range(8):
    #         for start_file in range(8):
    #             for end_rank in range(8):
    #                 for end_file in range(8):
    #                     combined_probs[start_rank, start_file, end_rank, end_file, piece_type] = \
    #                         piece_probs[piece_type] * move_probs[start_rank, start_file, 0] * move_probs[end_rank, end_file, 1]
                    
    # print(np.unravel_index(np.argmax(combined_probs, axis=None), combined_probs.shape))
    # best_move_indices = np.unravel_index(np.argmax(combined_probs, axis=None), combined_probs.shape)
    # start_rank, start_file, end_rank, end_file, best_piece_type = best_move_indices
    best_piece_type = np.argmax(piece_probs)

    # Step 2: Predict and mask moves for the selected piece
    best_piece_model = piece_models[best_piece_type]
    move_probs = best_piece_model.predict(np.expand_dims(encoded_board, axis=0))[0]
    legal_move_mask = is_legal_move(fen, best_piece_type)
    masked_move_probs = move_probs * legal_move_mask

    # Step 3: Select the best move for the selected piece
    start_pos = np.unravel_index(np.argmax(masked_move_probs[:, :, 0], axis=None), (8, 8))
    end_pos = np.unravel_index(np.argmax(masked_move_probs[:, :, 1], axis=None), (8, 8))

    # Step 4: Convert indices to UCI move
    start_square = index_to_algebraic(start_pos[0], start_pos[1])
    end_square = index_to_algebraic(end_pos[0], end_pos[1])
    uci_move = start_square + end_square
    
    return uci_move
    
    

def is_legal_move(fen, piece_type):
    board = chess.Board(fen)
    mask = np.zeros((8, 8, 2), dtype=np.float32)
    piece_map = {'P': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K': 5}
    turn = board.turn  # True for white, False for black
    
    for move in board.legal_moves:
        from_square = move.from_square
        to_square = move.to_square
        
        piece = board.piece_at(from_square)
        
        if piece_map[piece.symbol().upper()] == piece_type and piece.color == turn:

            mask[chess.square_rank(from_square), chess.square_file(from_square), 0] = 1.0
            mask[chess.square_rank(to_square), chess.square_file(to_square), 1] = 1.0
    
    return mask

def index_to_algebraic(rank, file):
    return chr(file + ord('a')) + str(8 - rank)

# # Test cases
# test_cases = [
#     ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "e2e4"),
#     ("rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2", "Nf3"),
#     ("rnbqkbnr/pppp1ppp/8/4p3/3P4/8/PPP2PPP/RNBQKBNR b KQkq - 0 2", "Nc6"),
#     ("rnbqkbnr/pppp2pp/4p3/5p2/3P4/8/PPP2PPP/RNBQKBNR w KQkq - 0 3", "c4"),
#     ("rnbqkb1r/pppppppp/5n2/8/8/5NP1/PPPPPP1P/RNBQKB1R w KQkq - 2 3", "Bg2")
# ]

# for fen, popular_move in test_cases:
#     predicted_move = predict_next_move(fen)
#     print(f"Expected: {popular_move}, Predicted: {predicted_move}")

