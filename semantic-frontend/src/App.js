import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import LandingPage from "./components/landing.jsx";
import GraphsPage from "./components/graphs.jsx";
import AboutPage from "./components/about.jsx";
import FindingsPage from "./components/findings.jsx";

const theme = createTheme({
  palette: {
    primary: {
      main: "#232327",
    },
    secondary: {
      main: "#D4D5E2",
      light: "#e7eaf0",
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <div className="App">
        <Router>
          <Routes>
            <Route exact path="/" element={<LandingPage />} />
            <Route exact path="/graphs" element={<GraphsPage />} />
            <Route exact path="/about" element={<AboutPage />} />
            <Route exact path="/findings" element={<FindingsPage />} />
          </Routes>
        </Router>
      </div>
    </ThemeProvider>
  );
}

export default App;
