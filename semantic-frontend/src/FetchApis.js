import axios from "axios";

export async function FetchPrevData(query) {
  console.log("Pinging for prev with query " + query);
  const response = await axios.get(`/prev?query=${query}`);
  console.log(response);
  return response.data;
}

export async function FetchDocsData(query) {
  console.log("Pinging for docs with query " + query);
  const response = await axios.get(`/docs?query=${query}`);
  console.log(response);
  return response.data;
}

export async function FetchStatsData(query) {
  console.log("Pinging for stats with query " + query);
  const response = await axios.get(`/stats?query=${query}`);
  console.log(response);
  return response.data;
}
