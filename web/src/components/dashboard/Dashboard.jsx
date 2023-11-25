import React, { useState } from "react"
import Board from "./board/Board"
import Form from "./form/Form"
import { Grid } from "@mui/material"
import { Chess } from 'chess.js'
import Explanation from "./explanation/Explanation"



const Dashboard = () => {
  const [chess, setChess] = useState(new Chess())
  const [board, setBoard] = useState(chess.board())
  const [playerColor, setPlayerColor] = useState('w')
  const [selectedPiece, setSelectedPiece] = useState(null)
  const [highlighted, setHighlighted] = useState([])
  const [gameOver, setGameOver] = useState(false)

  const resetGame = () => {
    const newChess = new Chess()
    setChess(newChess)
    setBoard(newChess.board())
    setSelectedPiece(null)
    setHighlighted([])
    setGameOver(false)
  }

  const togglePlayerColor = () => {
    setPlayerColor(playerColor === 'w' ? 'b' : 'w')
    resetGame()
  }

  return (
    <Grid container justifyContent="center">
      <Grid item xs={0} sm={3} style={{ display: 'flex', justifyContent: 'center' }}>
        <Form resetGame={resetGame} playerColor={playerColor} togglePlayerColor={togglePlayerColor}/>
      </Grid>
      <Grid item xs={12} sm={6} style={{display: 'flex', justifyContent: 'center'}}>
        <Board
          chess={chess}
          board={board}
          selectedPiece={selectedPiece}
          highlighted={highlighted}
          gameOver={gameOver}
          setSelectedPiece={setSelectedPiece}
          setHighlighted={setHighlighted}
          setBoard={setBoard}
          setGameOver={setGameOver}
        />
      </Grid>
      <Grid item xs={12} sm={3} style={{display: 'flex', justifyContent: 'center'}}>
        <Explanation />
      </Grid>
    </Grid>
  )
}

export default Dashboard
