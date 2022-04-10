import React, { useState, useEffect } from "react";
import { Box, TextField, Select, MenuItem } from "@mui/material";
import { useTheme } from "@mui/material/styles";
import Navbar from "./Navbar";
import PrevGraph from "./PrevGraph";
import RelevantDocuments from "./docs";
import CorpusStatistics from "./stats";
import { FetchPrevData, FetchDocsData, FetchStatsData } from "../FetchApis";

const defaultPrev = [
  {
    x: [1, 2, 3, 4],
    y: [10, 15, 13, 17],
    text: ["a", "b", "c", "d"],
    type: "scatter",
    line: {
      shape: "spline",
      smoothing: 0.65,
      color: "black",
    },
  },
];
const defaultDocs = { "Enter a query for document relevances": "" };
const defaultStats = { "Enter a query for corpus statistics": "" };

const defaults = {
  prev: defaultPrev,
  docs: defaultDocs,
  stats: defaultStats,
};

const GetGraphData = (type, query, smoothing) => {
  if (query == "") {
    return defaults[type];
  }
  switch (type) {
    case "prev":
      return FetchPrevData(query)
        .then((js) => {
          return [
            {
              x: js.x,
              y: js.y,
              text: js.text,
              type: "scatter",
              line: {
                shape: "spline",
                smoothing: smoothing,
                color: "black",
              },
            },
          ];
        })
        .catch((e) => {
          console.log(e);
          return defaults.prev;
        });
    case "docs":
      return FetchDocsData(query)
        .then((js) => {
          return js;
        })
        .catch((e) => {
          console.log(e.message);
          return defaults.docs;
        });
    case "stats":
      return FetchStatsData(query)
        .then((js) => {
          return js;
        })
        .catch((e) => {
          console.log(e.message);
          return defaults.stats;
        });
    default:
      return {};
  }
};

const GraphsPage = () => {
  const [query, setQuery] = useState("");
  const [graph, setGraph] = useState("prev");
  const [smoothing, setSmoothing] = useState(0.65);
  const [prevData, setPrevData] = useState(defaults.prev);
  const [docData, setDocData] = useState(defaults.docs);
  const [statsData, setStatsData] = useState(defaults.stats);

  const theme = useTheme();

  const updateData = async (type) => {
    switch (type) {
      case "prev":
        const p = await GetGraphData("prev", query, smoothing);
        setPrevData(p);
        break;
      case "docs":
        const d = await GetGraphData("docs", query, smoothing);
        setDocData(d);
        break;
      case "stats":
        const s = await GetGraphData("stats", query, smoothing);
        setStatsData(s);
        break;
    }
  };

  const handleChangeQuery = (e) => {
    setQuery(e.target.value);
  };

  const handleChangeGraph = (e) => {
    setGraph(e.target.value);
    updateData(e.target.value);
  };

  const GetGraph = (type) => {
    switch (type) {
      case "prev":
        return (
          <PrevGraph
            graphData={prevData}
            smoothing={smoothing}
            setSmoothing={setSmoothing}
            prevData={prevData}
            setPrevData={setPrevData}
          />
        );
      case "docs":
        return <RelevantDocuments docData={docData} />;
      case "stats":
        return <CorpusStatistics statData={statsData} />;
      default:
        return <div>If you see this, there was a fucky wucky</div>;
    }
  };

  const keyPress = (e) => {
    if (e.keyCode == 13) {
      updateData(graph);
    }
  };

  useEffect(() => {
    setPrevData(
      (function (d) {
        d[0].line.smoothing = smoothing;
        return d;
      })(prevData)
    );
  }, [smoothing]);

  return (
    <React.Fragment>
      <Navbar />
      <div
        style={{
          margin: "20px 20% 0 20%",
          textAlign: "center",
        }}
      >
        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
            alignContent: "center",
          }}
        >
          <TextField
            fullWidth
            label="Search Query"
            placeholder="death"
            value={query}
            onChange={handleChangeQuery}
            onKeyDown={keyPress}
            sx={{
              backgroundColor: theme.palette.secondary.light,
              margin: "0 10px 0 0",
            }}
          />
          <Select
            value={graph}
            defaultValue={"prev"}
            autoWidth
            onChange={handleChangeGraph}
            sx={{
              backgroundColor: theme.palette.secondary.light,
              margin: "0 0 0 10px",
              minWidth: "200px",
            }}
          >
            <MenuItem value={"prev"}>Prevalence</MenuItem>
            <MenuItem value={"docs"}>Relevant Documents</MenuItem>
            <MenuItem value={"stats"}>Corpus Statistics</MenuItem>
          </Select>
        </Box>
      </div>
      <div style={{ margin: "20px 5% 20px 5%" }}> {GetGraph(graph)} </div>
    </React.Fragment>
  );
};

export default GraphsPage;
