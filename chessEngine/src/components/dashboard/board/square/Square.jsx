import React from 'react'
import Paper from '@mui/material/Paper'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faChessPawn, faChessRook, faChessBishop, faChessKnight, faChessQueen, faChessKing } from '@fortawesome/free-solid-svg-icons'

const pieceImages = {
  p: faChessPawn,
  r: faChessRook,
  b: faChessBishop,
  n: faChessKnight,
  q: faChessQueen,
  k: faChessKing
}

function Square({ square, onClick, bgColor }) {
  return (
    <Paper
      className="square"
      elevation={0}
      onClick={onClick}
      style={{
        backgroundColor: bgColor,
        width: '60px',
        height: '60px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        cursor: 'pointer',
        borderRadius: 0
      }}
    >
      {square && (<FontAwesomeIcon size='2x' icon={pieceImages[square.type]} color={square.color === 'w' ? 'white' : 'black'}/>
      )}
    </Paper>
  )
}

export default Square