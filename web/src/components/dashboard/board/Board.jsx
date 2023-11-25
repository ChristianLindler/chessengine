import React from "react"
import Square from "./square/Square"
import { Button, Grid } from "@mui/material"
import { useTheme } from "@emotion/react"

const letterMap = ["a", "b", "c", "d", "e", "f", "g", "h"]

const Board = ({
  chess,
  board,
  selectedPiece,
  highlighted,
  gameOver,
  setSelectedPiece,
  setHighlighted,
  setBoard,
  setGameOver,
}) => {
  const theme = useTheme()
  const moveSound = new Audio("/moveSound.mp3")
  const checkSound = new Audio("/checkSound.mp3")

  const getNotation = (row, col) => {
    return letterMap[col] + (8 - row)
  }

  const getIndices = (notation) => {
    return {
      row: 8 - Number(notation.charAt(1)),
      col: letterMap.indexOf(notation.charAt(0)),
    }
  }

  const getBgColor = (row, col) => {
    if (selectedPiece && selectedPiece[0] === row && selectedPiece[1] === col) {
      return theme.palette.highlight.main
    } else if (
      highlighted.some(
        (highlightedSquare) =>
          highlightedSquare.row === row && highlightedSquare.col === col
      )
    ) {
      return theme.palette.highlight.main
    } else {
      return (row + col) % 2 === 0
        ? theme.palette.secondary.light
        : theme.palette.secondary.main
    }
  }

  const getBotMove = async () => {
    const moves = chess.moves()
    const move = moves[Math.floor(Math.random() * moves.length)]
    chess.move(move)
    setBoard(chess.board())
  }

  const handleSquareClick = async (row, col) => {
    if (gameOver) return
    
    const clickedPiece = chess.get(getNotation(row, col))

    // If the user hasn't selected a piece, check if they are currently selecting a piece
    if (!selectedPiece) {
      if (clickedPiece && clickedPiece.color === chess.turn()) {
        setSelectedPiece([row, col])
        const moves = chess.moves({
          square: getNotation(row, col),
          verbose: true,
        })
        setHighlighted(moves.map((move) => getIndices(move.to)))
      }
    
    } else {
      // If we have selected a piece, check if the clicked square is currently highlightes
      const isValidMove = highlighted.some(
        (highlightedSquare) =>
          highlightedSquare.row === row && highlightedSquare.col === col
      )

      // If it is highlighted, make a move
      if (isValidMove) {
        chess.move(
          getNotation(selectedPiece[0], selectedPiece[1]) +
            getNotation(row, col)
        )

        if (chess.isCheck()) {
          checkSound.play()
        } else {
          moveSound.play()
        }
        
        setBoard(chess.board())
        
        // Check for game over, then make bot move.
        if (chess.isCheckmate()) {
          setGameOver(true)
        } else {
          await getBotMove()
          setBoard(chess.board())
          if (chess.isCheckmate()) setGameOver(true)
        }
      }

      setSelectedPiece(null)
      setHighlighted([])
    }
  }
  

  return (
    <div style={{ display: "flex", flexDirection: "column" }}>
      {board.map((row, rowIndex) => (
        <div key={rowIndex} style={{ display: "flex" }}>
          {row.map((square, colIndex) => (
            <div key={colIndex}>
              <Square
                square={square}
                onClick={() => handleSquareClick(rowIndex, colIndex)}
                bgColor={getBgColor(rowIndex, colIndex)}
              />
            </div>
          ))}
        </div>
      ))}
    </div>
  )
}

export default Board
