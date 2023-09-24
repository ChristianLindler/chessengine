import Board from "./components/board/Board"
import { createTheme, CssBaseline, ThemeProvider } from "@mui/material"
import Header from "./components/header/Header"

const theme = createTheme({
  palette: {
    secondary: {
      main: '#002C71',
      light: '#C3C3E4'
    },
    highlight: {
      main: '#89CFF0'
    }
  }
})

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Header/>
      <div style={{paddingTop: '20px', display: 'flex', justifyContent: 'center'}}>
        <Board />
      </div>
    </ThemeProvider>
  )
}

export default App
