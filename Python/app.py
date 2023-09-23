from flask import Flask, request, jsonify

app = Flask(__name__)

chessboard = None

@app.route('/update-chessboard', methods=['POST'])
def update_chessboard():
    data = request.json
    chessboard = data.get('chessboard')
    return

if __name__ == '__main__':
    app.run(debug=True)

def get_chessboard():
    return chessboard
