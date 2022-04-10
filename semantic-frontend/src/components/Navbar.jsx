import React from "react";
import { Link } from "react-router-dom";
import { AppBar, Toolbar, Typography, Button, IconButton } from "@mui/material";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";

const Navbar = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Link to="/">
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
          >
            <Typography variant="h6" component="div" sx={{ flex: 1 }}>
              Semantic Evolution
            </Typography>
          </IconButton>
        </Link>
        <div style={{ marginLeft: "auto" }}>
          <Link to="/graphs">
            <Button color="inherit">Graphs</Button>
          </Link>
          <Link to="/about">
            <Button color="inherit">About</Button>
          </Link>
          <Link to="/findings">
            <Button color="inherit">Findings</Button>
          </Link>
          <a
            href="https://github.com/gholmes829/TheBigDogSemanticsModule"
            target="_blank"
          >
            <Button color="inherit">
              Source{" "}
              <OpenInNewIcon fontSize="inherit" className="material-icons" />{" "}
            </Button>
          </a>
        </div>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
