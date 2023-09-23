import { Grid, Paper } from '@mui/material'
import { useState } from 'react'

const ChessBoard = () => {
  const [board, setBoard] = useState([
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
  ])

  return (
    <Grid container spacing={0}>
      {board.map((row, rowIndex) => (
        <Grid container item key={rowIndex} margin={0} xs={8}>
          {row.map((col, colIndex) => (
            <Grid item key={colIndex} xs={1}>
              <Paper
                style={{
                  height: '50px',
                  width: '50px',
                  backgroundColor:
                    (rowIndex + colIndex) % 2 === 0 ? 'white' : 'black',
                }}
              >
               {/* You can add chess pieces here */}
              </Paper>
            </Grid>
          ))}
        </Grid>
      ))}
    </Grid>
  )
}

export default ChessBoard