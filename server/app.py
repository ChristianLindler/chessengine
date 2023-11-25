from cnn.predict_move import predict_next_move
from flask import Flask, request, jsonify

app = Flask(__name__)

chessboard = None

@app.route('/get_move', methods=['POST'])
def get_move():
    data = request.json
    fen = data.get('fen')
    return predict_next_move(fen)

if __name__ == '__main__':
    app.run(debug=True)

