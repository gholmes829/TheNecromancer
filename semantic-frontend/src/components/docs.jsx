import React from "react";
import { Typography } from "@mui/material";

const RelevantDocuments = (props) => {
  const { docData } = props;

  return Object.entries(docData).map((pair, idx) => {
    return (
      <div key={idx} style={{ textAlign: "center" }}>
        <Typography variant="h6" gutterBottom>
          {pair[0]}: {pair[1]}
        </Typography>{" "}
      </div>
    );
  });
};

export default RelevantDocuments;
