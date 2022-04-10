import React from "react";
import { Typography } from "@mui/material";

const CorpusStatistics = (props) => {
  const { statData } = props;

  return Object.entries(statData.values).map((val, idx) => {
    return (
      <div key={idx} style={{ textAlign: "center" }}>
        <Typography variant="h6" gutterBottom>
          {val[1]}
        </Typography>
      </div>
    );
  });
};

export default CorpusStatistics;
