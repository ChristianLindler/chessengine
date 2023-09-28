import React from "react"
import { Grid, Paper, useTheme } from "@mui/material"

const Explanation = () => {
  const theme = useTheme()
  return (
    <Paper style={{ background: theme.palette.secondary.light, padding: "16px", width: '100%' }}>
      <Grid container spacing={2} alignItems="center">
        <Grid item xs={12}>
          <h1>Behind the Models</h1>
        </Grid>
        <Grid item xs={12}>
          <h3>Neural Net</h3>
          <p>neruelarea dadslgadbs dbfahds twhe tsbdk dsfads fadsasdfasdfadfasd</p>
        </Grid>
        <Grid item xs={12}>
          <h3>Minimax</h3>
          <p>neruelarea dadslgadbs dbfahds twhe tsbdkadsfadsfasdfadfadsfadasdfasdfasdf</p>
        </Grid>
      </Grid>
    </Paper>
  )
}

export default Explanation