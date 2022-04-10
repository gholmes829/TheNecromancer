import React from "react";
import { Typography } from "@mui/material";

const CorpusStatistics = (props) => {
  const { statData } = props;

  return Object.entries(statData).map((pair, idx) => {
    return (
      <div key={idx} style={{ textAlign: "center" }}>
        <Typography variant="h6" gutterBottom>
          {pair[0]}: {pair[1]}
        </Typography>
      </div>
    );
  });
};

export default CorpusStatistics;
