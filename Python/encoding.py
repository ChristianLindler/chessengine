import numpy as np
import tqdm

def encode_board(fen):
    encoded = np.zeros((8, 8, 20))
    
    parts = fen.split()
    board, turn, castling, en_passant, halfmove, fullmove = parts
    
    rows = board.split('/')
    for row_idx, row in enumerate(rows):
        col_idx = 0
        for char in row:
            if char.isdigit():
                col_idx += int(char)
            else:
                plane_idx = {
                    'P': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K': 5, # White pieces
                    'p': 6, 'n': 7, 'b': 8, 'r': 9, 'q': 10, 'k': 11 
                }[char]
                encoded[row_idx, col_idx, plane_idx] = 1
                col_idx += 1
    
    # Encode turn
    encoded[:, :, 12] = 1 if turn == 'w' else 0
    
    # Encode castling rights
    encoded[:, :, 13] = 1 if 'K' in castling else 0
    encoded[:, :, 14] = 1 if 'Q' in castling else 0
    encoded[:, :, 15] = 1 if 'k' in castling else 0
    encoded[:, :, 16] = 1 if 'q' in castling else 0
    
    # Encode en passant target square
    if en_passant != '-':
        row, col = 8 - int(en_passant[1]), ord(en_passant[0]) - ord('a')
        encoded[row, col, 17] = 1
    
    
    return encoded

def encode_move(uci):
    #encode move from uci string
    encoded = np.zeros((8, 8, 2))
    
    # Extract start and end squares
    start, end = uci[:2], uci[2:]

    row, col = 8 - int(start[1]), ord(start[0]) - ord('a')
    encoded[row, col, 0] = 1
    
    row, col = 8 - int(end[1]), ord(end[0]) - ord('a')
    encoded[row, col, 1] = 1
    
    return encoded

def decode_move(encoded_move):
    start_plane = encoded_move[:, :, 0]
    end_plane = encoded_move[:, :, 1]
    
    start_idx = np.unravel_index(np.argmax(start_plane, axis=None), start_plane.shape)
    end_idx = np.unravel_index(np.argmax(end_plane, axis=None), end_plane.shape)
    
    start_square = chr(start_idx[1] + ord('a')) + str(8 - start_idx[0])
    end_square = chr(end_idx[1] + ord('a')) + str(8 - end_idx[0])
    
    uci_move = start_square + end_square
    
    return uci_move

def encode_piece_type(piece_type):
    # One-hot encode the piece type
    encoded = np.zeros(6)
    encoded[piece_type - 1] = 1
    return encoded

