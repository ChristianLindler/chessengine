# Chess Move Predictor

A machine learning project that predicts the next move in a chess game based on the current board state.

## Overview

This project utilizes a unique approach by employing a set of Convolutional Neural Networks (CNNs) to predict the next move in a chess game. The model is trained on a dataset of historical chess games, encoded in the FEN (Forsyth-Edwards Notation) format, with the predicted moves returned in UCI (Universal Chess Interface) format.

## Features

### Board and Move Encoding
- **Board Encoding**: The `encode_board` function converts FEN strings to a plane-based encoding suitable for neural network input.
- **Move Encoding**: The `encode_move` function converts UCI move strings to a plane-based encoding for model output.

### Neural Network Model
The project features a set of 7 CNNs, each designed for a specific task in the chess move prediction process:

- **Piece Selection Model**: The primary CNN is responsible for selecting which piece to move. This model is trained to predict the type of piece that should be moved next, based on the current board state represented by the encoded FEN string.

- **Piece-Specific Models**: For each of the six chess pieces (Pawn, Knight, Bishop, Rook, Queen, King), there is a dedicated CNN model. Each of these models is trained to predict the best move for its respective piece. The predictions from these models are combined to determine the final move prediction.

### Move Prediction and Validation
- The `predict_next_move` function in `predict_move.py` is the main function for move prediction. It loads the piece selection model and all piece-specific models. It then predicts the piece to move and calculates the move probabilities for each piece, applying a legal move mask to ensure validity. The function selects the best move for the predicted piece and converts the indices to a UCI move.

- **Legal Move Masking**: The `is_legal_move` function generates a mask to filter out illegal moves for the predicted piece, ensuring that the final move prediction is valid.

### Model Training
- The `model.py` file contains the code for creating and training the CNN models. The `create_cnn_model` function establishes the architecture of the CNNs, with layers optimized for the task of chess move prediction. The models are trained using a dataset of encoded board states and moves, with early stopping implemented to prevent overfitting. Specifics of the model can be found in `model.py`.

## Frontend Implementation
The Chess Move Predictor also features a React-based frontend that provides a user-friendly interface for interacting with the prediction models:

- **React Frontend**: The frontend is implemented using React, providing a dynamic and responsive user interface. Users can interact with a visual chess board, inputting the current game state and receiving move predictions in real-time.

- **Flask API Integration**: The React frontend communicates with the backend prediction models through a Flask API. This API serves as the intermediary between the frontend and the backend, receiving requests from the React application, processing the requests with the prediction models, and returning the predicted moves to the frontend.
