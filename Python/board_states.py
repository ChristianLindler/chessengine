import chess.pgn

def list_games():
    #read games from pgn file
    with open("chess.pgn") as pgn_file:
        games = []
        game_count = 0
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None or game_count > 5000: 
                break
            games.append(game)
            game_count += 1
    return games


def fen_games():
    #convert games to fen and moves to uci
    X = [] #games in FEN
    Y = [] #moves in UCI
    games = list_games()
    for game in games:
        board = game.board()
        for move in game.mainline_moves():
            X.append(board.fen())
            Y.append(move.uci())
            board.push(move)
    return X, Y
