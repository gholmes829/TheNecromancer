import React from "react";
import Plot from "react-plotly.js";
import { Slider } from "@mui/material";
import { useTheme } from "@mui/material/styles";
import MovingIcon from "@mui/icons-material/Moving";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";

const PrevGraph = (props) => {
  const theme = useTheme();
  const { graphData, smoothing, setSmoothing } = props;
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "normal",
        alignContent: "center",
        height: "75vh",
      }}
    >
      <Plot
        data={graphData}
        style={{ height: "100%" }}
        layout={{
          autoMargin: true,
          title: "Prevalence over Time",
          xaxis: {
            title: {
              text: "Time",
            },
          },
          yaxis: {
            title: {
              text: "Prevalence",
            },
          },
          plot_bgcolor: theme.palette.secondary.light,
          paper_bgcolor: theme.palette.secondary.light,
        }}
      />{" "}
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          justifyContent: "center",
          alignContent: "center",
          margin: "20px 0 0 0",
        }}
      >
        <TrendingUpIcon fontSize="large" />
        <Slider
          aria-label="Smoothing"
          defaultValue={0}
          min={0}
          max={130}
          value={smoothing * 100}
          onChange={(e, s) => {
            setSmoothing(s / 100);
          }}
          sx={{ margin: "0 20px 0 20px" }}
        />
        <MovingIcon fontSize="large" />
      </div>
    </div>
  );
};

export default PrevGraph;
