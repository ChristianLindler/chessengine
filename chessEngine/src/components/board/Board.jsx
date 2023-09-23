import { useState } from 'react'
import Square from './square/Square'
import { Chess } from 'chess.js'

const letterMap = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

const Board = () => {
  const [chess] = useState(new Chess())
  const [selectedPiece, setSelectedPiece] = useState(null)
  const [highlighted, setHighlighted] = useState([])
  const [board, setBoard] = useState(chess.board())

  const getNotation = (row, col) => {
    return letterMap[col] + (8 - row)
  }

  const getIndices = (notation) => {
    return {row: 8 - Number(notation.charAt(1)), col: letterMap.indexOf(notation.charAt(0))}
  }

  const getBgColor = (row, col) => {
    if (selectedPiece && selectedPiece[0] === row && selectedPiece[1] === col) {
      return 'red'
    } else if (highlighted.some((highlightedSquare) => highlightedSquare.row === row && highlightedSquare.col === col)) {
      return 'orange'
    } else {
      return (row + col) % 2 === 0 ? 'gray' : '#1E3054'
    }
  }

  const handleSquareClick = (row, col) => {
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
      }
      setSelectedPiece(null)
      setHighlighted([])
      setBoard(chess.board())
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
    </div>
  )
}

export default Board