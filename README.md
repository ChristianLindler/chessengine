# Chess Move Predictor

A machine learning project that predicts the next move in a chess game based on the current board state.

## Overview

This project uses a Convolutional Neural Network (CNN) to predict the next move in a chess game. The model is trained on a dataset of historical chess games, encoded in the FEN (Forsyth-Edwards Notation) format. The predicted moves are returned in UCI (Universal Chess Interface) format.

## Features

- **Board Encoding**: Converts FEN strings to a plane-based encoding suitable for neural network input.
- **Move Encoding**: Converts UCI move strings to a plane-based encoding for model output.
- **Neural Network Model**: A simple CNN architecture implemented using TensorFlow and Keras.
- **Move Validation**: Uses the `python-chess` library to validate if the predicted move is legal.
