import React from "react";
import { Box, Typography } from "@mui/material";

import Navbar from "./Navbar";

const AboutPage = () => {
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
          We train our own custom word embeddings using the FastText algorithm on our corpus of over 80
          gothic and romantic novels, poems, and other textual mediums from a time period of over 100
          years. We can then find how "similar" terms are with each other by computing cosine similarity
          between vectors representing different terms in our corpus' vocabulary. In this sense, we can compare
          processed tokens from a query to relevant from documents to create a semnatically grounded prevalence score.
          We must heavily preprocess the corpus, employing a variety of tokenizers, stemmers,
          and other natural language processing tools. Basing our search engine on the classic
          vector space model with inverted index, we can easily resolve the most relevant documents
          to a given query. We combine these techniques to create an intuitve, interesting, and insightful presentation
          of how semantic meaning changes over time for this influential movement.
        </Typography>
      </Box>
    </React.Fragment>
  );
};

export default AboutPage;
