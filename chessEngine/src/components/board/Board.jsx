import { useState } from 'react'
import Square from './square/Square'
import { Chess } from 'chess.js'
import { Button, Grid } from '@mui/material'
import { useTheme } from '@emotion/react'

const letterMap = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

const Board = () => {
  const theme = useTheme()
  const [chess] = useState(new Chess())
  const [selectedPiece, setSelectedPiece] = useState(null)
  const [highlighted, setHighlighted] = useState([])
  const [board, setBoard] = useState(chess.board())
  const [gameOver, setGameOver] = useState(false)
  const audio = new Audio('/moveSound.mp3')

  const getNotation = (row, col) => {
    return letterMap[col] + (8 - row)
  }

  const getIndices = (notation) => {
    return {row: 8 - Number(notation.charAt(1)), col: letterMap.indexOf(notation.charAt(0))}
  }

  const resetGame = () => {
    chess.reset()
    setBoard(chess.board())
  }

  const getBgColor = (row, col) => {
    if (selectedPiece && selectedPiece[0] === row && selectedPiece[1] === col) {
      return theme.palette.highlight.main
    } else if (highlighted.some((highlightedSquare) => highlightedSquare.row === row && highlightedSquare.col === col)) {
      return theme.palette.highlight.main
    } else {
      return (row + col) % 2 === 0 ? theme.palette.secondary.light : theme.palette.secondary.main
    }
  }

  const getBotMove = async() => {
    try {
      const response = await fetch('url of bot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          fen: chess.fen()
        }),
      })

      if (!response.ok) {
        throw new Error('Network response was not ok')
      }
      const data = await response.json()
      chess.move(data.move)
      setBoard(chess.board)
    } catch (error) {
      console.error('Error calculating move: ', error)
    }
  }

  const handleSquareClick = (row, col) => {
    if (gameOver) return
    const clickedPiece = chess.get(getNotation(row, col))

    if (!selectedPiece) {
      if (clickedPiece && clickedPiece.color === chess.turn()) {
        setSelectedPiece([row, col])
        const moves = chess.moves({ square: getNotation(row, col), verbose: true })
        setHighlighted(moves.map(move => getIndices(move.to)))
      }
    } else {
      if (highlighted.some((highlightedSquare) => highlightedSquare.row === row && highlightedSquare.col === col)) {
        chess.move(getNotation(selectedPiece[0], selectedPiece[1]) + getNotation(row, col))
        audio.play()
        setBoard(chess.board())
      }
      setSelectedPiece(null)
      setHighlighted([])

      if (chess.isCheckmate()) {
        setGameOver(true)
      } else {
        getBotMove()
        audio.play()
        setBoard(chess.board())
        if (chess.isCheckmate()) setGameOver(true)
      }
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column' }}>
      {board.map((row, rowIndex) => (
        <div key={rowIndex} style={{ display: 'flex' }}>
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
      <Grid container>
        <Grid item xs={3}>
          <Button onClick={resetGame} style={{backgroundColor: theme.palette.secondary.light, color: 'white'}}>Reset</Button>
        </Grid>
      </Grid>
    </div>
  )
}

export default Board