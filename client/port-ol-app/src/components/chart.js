import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';


// new es 6 style
// use class if the comp will have an inner state


// does this have to be class-vbased?
//  is it anough to be like video_detail?
const Chart = (props) => {
  console.log("RENDERING CHART? w props: " + props);
  console.log("props.data: ")
  console.log(props.data);
  const data = props.data;

  if (!data) {
    return <div> No data to show... </div>
  }
  if (data.length === 0) {
    return <div> Empty data ... </div>
  }

  return (
    <BarChart width={800} height={400} data={data}
          margin={{top: 5, right: 30, left: 20, bottom: 5}}>
     <XAxis dataKey="label"/>
     <YAxis/>
     <CartesianGrid strokeDasharray="3 3"/>
     <Tooltip/>
     <Legend />
     <Bar dataKey="outlier" stackId="all" fill="#1BBBBB" />
     <Bar dataKey="normal" stackId="all" fill="#BBBBBB" />
    </BarChart>
  );
};

Chart.propTypes = {
  data: React.PropTypes.array.isRequired,
};

export default Chart;
