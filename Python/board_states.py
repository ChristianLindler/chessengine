import chess.pgn
from tqdm import tqdm, trange

def list_games():
    #read games from pgn file
    with open("chess.pgn") as pgn_file:
        games = []
        game_count = 0
        print("Reading games from pgn file...")
        for game_count in trange(10000):
            game = chess.pgn.read_game(pgn_file)
            if game is None: 
                break
            games.append(game)
            game_count += 1
    return games


def fen_games():
    #convert games to fen and moves to uci
    X = [] #games in FEN
    Y = [] #moves in UCI
    Z = [] #piece types
    games = list_games()
    print("Building boards from moves...")
    for game in tqdm(games):
        board = game.board()
        for move in game.mainline_moves():
            X.append(board.fen())
            Y.append(move.uci())
            piece_type = get_piece_type_from_uci(board.fen(), move.uci())
            Z.append(piece_type)
            board.push(move)
    return X, Y, Z

def get_piece_type_from_uci(fen, uci_move):
    board = chess.Board(fen)
    move = chess.Move.from_uci(uci_move)
    piece = board.piece_at(move.from_square)
    return piece.piece_type - 1

# Example usage:
# fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
# uci_move = "e2e4"
# piece_type = get_piece_type_from_uci(fen, uci_move)

# # Convert piece type to string for clarity
# piece_name = chess.piece_name(piece_type)
# print(piece_name)  # Outputs: "pawn"
