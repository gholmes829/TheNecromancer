import React from "react";
import { Box, Button, Typography } from "@mui/material";
import { Link } from "react-router-dom";
import Navbar from "./Navbar";

const LandingPage = () => {
  return (
    <React.Fragment>
      <Navbar />
      <Box
        sx={{
          margin: "20px 10% 0 10%",
          display: "flex",
          justifyContent: "center",
          alignContent: "center",
          textAlign: "center",
        }}
      >
        <Typography variant="subtitle1" gutterBottom>
          Welcome to 💀The Necromancer💀 <br /> by Connor Sutton, Grant Holmes,
          and Daniel Johnson <br /> <br /> This work aims to aid with knowledge
          discovery of literary works and movements. On the{" "}
          <Link style={{ color: "blue" }} to="/graphs">
            "graphs"
          </Link>{" "}
          page, you can input a search query which then gets processed using
          Natural Language Processing (NLP) and Information Retreival (IR) over
          an expertly-crafted corpus of gothic and romantic literature.
        </Typography>
      </Box>
    </React.Fragment>
  );
};

export default LandingPage;
