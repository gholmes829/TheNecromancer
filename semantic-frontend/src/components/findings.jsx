import React from "react";
import { Box, Typography } from "@mui/material";

import Navbar from "./Navbar";

const FindingsPage = () => {
  return (
    <React.Fragment>
      <Navbar />
      <Box
        sx={{
          margin: "20px 20% 0 20%",
          display: "flex",
          justifyContent: "center",
          alignContent: "center",
          textAlign: "center",
        }}
      >
        <Typography variant="subtitle1" gutterBottom>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut labore et dolore magna aliqua. Vestibulum
          sed arcu non odio euismod. Sem et tortor consequat id. Odio
          pellentesque diam volutpat commodo. Diam quis enim lobortis
          scelerisque fermentum dui faucibus in ornare. Sed viverra ipsum nunc
          aliquet bibendum enim. Varius vel pharetra vel turpis nunc. Sed odio
          morbi quis commodo odio. Aliquam vestibulum morbi blandit cursus risus
          at. Enim blandit volutpat maecenas volutpat blandit aliquam etiam erat
          velit. Mauris nunc congue nisi vitae suscipit tellus mauris. In
          pellentesque massa placerat duis ultricies lacus sed turpis tincidunt.
        </Typography>
      </Box>
    </React.Fragment>
  );
};

export default FindingsPage;
