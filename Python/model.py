import numpy as np
import tensorflow as tf

from sklearn.model_selection import train_test_split
from board_states import fen_games, get_piece_type_from_uci
from encoding import encode_board, encode_move
from tqdm import tqdm

def create_cnn_model(input_shape, num_output_units):
    model = tf.keras.models.Sequential([
        # Convolutional layer with 32 filters
        tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu', padding='same', input_shape=input_shape,
                               kernel_initializer=tf.keras.initializers.RandomNormal(stddev=1e-7), 
                               kernel_regularizer=tf.keras.regularizers.l2(0.0001)),
        tf.keras.layers.BatchNormalization(),
        
        # Convolutional layer with 64 filters
        tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same',
                               kernel_initializer=tf.keras.initializers.RandomNormal(stddev=1e-6), 
                               kernel_regularizer=tf.keras.regularizers.l2(0.0001)),
        tf.keras.layers.BatchNormalization(),
        
        # Flatten the output
        tf.keras.layers.Flatten(),
        
        # Dense layer with 256 units and ReLU activation
        tf.keras.layers.Dense(256, activation='relu', 
                              kernel_initializer=tf.keras.initializers.RandomNormal(stddev=1e-6), 
                              kernel_regularizer=tf.keras.regularizers.l2(0.0001)),
        tf.keras.layers.BatchNormalization(),
        
        # Output layer with softmax activation
        tf.keras.layers.Dense(num_output_units, activation='softmax',
                              kernel_initializer=tf.keras.initializers.RandomNormal(stddev=1e-6), 
                              kernel_regularizer=tf.keras.regularizers.l2(0.0001)),
        
        tf.keras.layers.Reshape((8, 8, 2)) if num_output_units == 8*8*2 else tf.keras.layers.Lambda(lambda x: x)
    ])
    
    # Compile the model with RMSprop optimizer
    model.compile(optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.0015, weight_decay=0.999), 
                  loss='categorical_crossentropy', 
                  metrics=['accuracy'])
    
    return model

# Callbacks
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

def filter_dataset_by_piece_type(games, moves, piece_types, target_piece_type):
    filtered_games = []
    filtered_moves = []
    for game, move, piece_type in zip(games, moves, piece_types):
        if piece_type == target_piece_type:
            filtered_games.append(game)
            filtered_moves.append(move)
    return filtered_games, filtered_moves

def train_piece_selection_model(games, moves):
    encoded_boards = [encode_board(board) for board in tqdm(games)]
    piece_types = [get_piece_type_from_uci(game, move) for game, move in tqdm(zip(games, moves), total=len(games))]
    piece_types_onehot = tf.keras.utils.to_categorical(piece_types, num_classes=6)

    encoded_boards = np.array(encoded_boards)

    # Split the data
    X_train, X_val, y_train, y_val = train_test_split(encoded_boards, piece_types_onehot, test_size=0.2, random_state=42)

    # Create and compile the model
    model = create_cnn_model(X_train.shape[1:], 6)  # 6 output units for 6 piece types
    
    # Train the model
    model.fit(X_train, y_train, epochs=15, batch_size=250, validation_data=(X_val, y_val), 
            callbacks=[early_stopping])
    model.save('piece_selection_model.keras')

def train_model_for_piece(games, moves, piece_types, piece_type):
    filtered_games, filtered_moves = filter_dataset_by_piece_type(games, moves, piece_types, piece_type)
    
    encoded_boards = [encode_board(game) for game in tqdm(filtered_games)]
    encoded_moves = [encode_move(move) for move in tqdm(filtered_moves)]


    encoded_boards = np.array(encoded_boards)
    encoded_moves = np.array(encoded_moves)

    # Split the data
    X_train, X_val, y_train, y_val = train_test_split(encoded_boards, encoded_moves, test_size=0.2, random_state=42)

    # Create and compile the model
    model = create_cnn_model(X_train.shape[1:], 8*8*2)  # 8*8*2 output units for moves
    
    # Train the model
    model.fit(X_train, y_train, epochs=15, batch_size=250, validation_data=(X_val, y_val), 
            callbacks=[early_stopping])
    model.save(f'chess_model_for_piece_{piece_type}.keras')

# Load the games and moves once
games, moves, piece_types = fen_games()

# Train the piece selection model
train_piece_selection_model(games, moves)

# Train the models for each piece type
for piece_type in range(6):
    train_model_for_piece(games, moves, piece_types, piece_type)
