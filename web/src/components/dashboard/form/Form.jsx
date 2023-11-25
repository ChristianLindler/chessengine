import React from "react"
import { Button, Grid, Paper, Select, MenuItem, InputLabel, useTheme, RadioGroup, FormControlLabel, Radio } from "@mui/material"

const Form = ({ resetGame, pieceColor, togglePieceColor }) => {
  const theme = useTheme()
  return (
    <Paper style={{ background: theme.palette.secondary.light, padding: "16px", width: '100%' }}>
      <Grid container spacing={2} alignItems="center">
        <Grid item xs={12}>
          <h1>Chess Parameters</h1>
        </Grid>
        <Grid item xs={12}>
          <InputLabel>Select Model</InputLabel>
          <Select label="Select Model" style={{ width: '100%' }}>
            <MenuItem value="NeuralNet">Neural Net</MenuItem>
              <MenuItem value="Minimax">Minimax</MenuItem>
          </Select>
        </Grid>
        <Grid item xs={12}>
          <RadioGroup row value={pieceColor} onChange={togglePieceColor}>
            <FormControlLabel
              value="w"
              control={<Radio color="primary" />}
              label="White"
            />
            <FormControlLabel
              value="b"
              control={<Radio color="primary" />}
              label="Black"
            />
          </RadioGroup>
        </Grid>
        <Grid item xs={12}>
          <Button
            variant="contained"
            color="primary"
            onClick={resetGame}
            style={{width: '100%'}}
          >
            New Game
          </Button>
        </Grid>
      </Grid>
    </Paper>
  )
}

export default Form