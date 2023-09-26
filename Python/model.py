import numpy as np
import tensorflow as tf

from sklearn.model_selection import train_test_split
from board_states import fen_games
from encoding import encode_board, encode_move
from tqdm import tqdm

def train_model():
    games, moves = fen_games()
    encoded_boards = []
    encoded_moves = []

    print("Encoding games...")
    for board in tqdm(games):
        encoded_boards.append(encode_board(board))
    print("Encoding moves...")
    for move in tqdm(moves):
        encoded_moves.append(encode_move(move))

    encoded_boards = np.array(encoded_boards)
    encoded_moves = np.array(encoded_moves)
        
    model = tf.keras.models.Sequential([
        # Convolutional layer with 32 features followed by ReLU activation
        tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu', padding='same', input_shape=(8,8,20), kernel_regularizer=tf.keras.regularizers.l2(0.0001)),
        
        # Flatten the output to feed into fully connected layers
        tf.keras.layers.Flatten(),
        
        # First fully connected (affine) layer with 128 units
        tf.keras.layers.Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.0001)),
        
        # Second fully connected (affine) layer with 128 units
        tf.keras.layers.Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.0001)),
        
        # Output layer with softmax activation
        tf.keras.layers.Dense(8 * 8 * 2, activation='softmax'),
        
        # Reshape to match the desired output shape
        tf.keras.layers.Reshape((8,8,2))
    ])

    X_train, X_val, y_train, y_val = train_test_split(encoded_boards, encoded_moves, test_size=0.2, random_state=42)

    optimizer = tf.keras.optimizers.RMSprop(lr=0.0015, decay=0.999)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    
    model.fit(X_train, y_train, 
              epochs=15, 
              batch_size=250, 
              validation_data=(X_val, y_val),
              callbacks=[early_stopping])

    model.save('chess_model.keras')

train_model()
