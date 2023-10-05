import React from 'react';
import Plot from 'react-plotly.js';

const MyPlot = () => {
  const data = [
    {
      x: [1, 2, 3, 4, 5],
      y: [1, 2, 4, 8, 16],
      type: 'scatter',
    },
  ];

  const layout = {
    title: 'My Plot',
    xaxis: { title: 'X-axis' },
    yaxis: { title: 'Y-axis' },
  };

  return <Plot data={data} layout={layout} />;
};

export default MyPlot;
