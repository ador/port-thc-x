import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';


const Chart = (props) => {

  const data = props.data;

  if (!data) {
    return <div> No data to show... </div>
  }
  if (data.length === 0) {
    return <div> Empty data ... </div>
  }

  return (
    <BarChart width={600} height={400} data={data}
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
