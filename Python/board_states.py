import chess.pgn

games = []
def list_games():
    #read games from pgn file
    with open('chess.pgn') as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break
            games.append(game)
    return games

X = [] #games in FEN
Y = [] #moves in UCI

def fen_games():
    #convert games to fen and moves to uci
    games = list_games()
    for game in games:
        board = game.board()
        for move in game.mainline_moves():
            X.append(board.fen())
            Y.append(move.UCI)
            board.push()
    return X, Y
