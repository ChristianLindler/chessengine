import React from 'react'
import { AppBar, Toolbar, Button } from '@mui/material'
import { useTheme } from '@emotion/react'

const Header = () => {
  const theme = useTheme()
  return (
    <AppBar position='static'>
      <Toolbar style={{backgroundColor: theme.palette.secondary.main}}>
        <h1>
          Chess Engine
        </h1>
        <a href='https://github.com/ChristianLindler/optionspricer' style={{color: 'white'}}>GitHub</a>
      </Toolbar>
    </AppBar>
  )
}

export default Header