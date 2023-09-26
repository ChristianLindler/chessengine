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
    games = list_games()
    print("Building boards from moves...")
    for game in tqdm(games):
        board = game.board()
        for move in game.mainline_moves():
            X.append(board.fen())
            Y.append(move.uci())
            board.push(move)
    return X, Y
