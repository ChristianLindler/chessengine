import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from board_states import fen_games
from encoding import encode_board, encode_move

def train_model():
    games, moves = fen_games()
    encoded_boards = []
    encoded_moves = []

    for board in games:
        encoded_boards.append(encode_board(board))
    for move in moves:
        encoded_moves.append(encode_move(move))

    encoded_boards = np.array(encoded_boards)
    encoded_moves = np.array(encoded_moves)
        
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu', padding='same', input_shape=(8,8,20)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(8 * 8 * 2, activation='softmax'),
        tf.keras.layers.Reshape(8,8,2)
    ])

    X_train, X_val, y_train, y_val = train_test_split(encoded_boards, encoded_moves, test_size=0.2, random_state=42)

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    model.fit(X_train, y_train, epochs=5, batch_size=32, validation_split=0.2)

    model.save('chess_model.h5')