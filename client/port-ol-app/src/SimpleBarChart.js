//const {BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend} = Recharts;
import React, { Component } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const data = [
      {label: '10.0 - 16.2 ', outlier: 9, normal: 0},
      {label: '16.2 - 22.4 ', outlier: 5, normal: 5},
      {label: '22.4 - 28.6 ', outlier: 0, normal: 20},
      {label: '28.6 - 34.8 ', outlier: 0, normal: 50},
      {label: '34.8 - 43.0 ', outlier: 0, normal: 50}
];

class SimpleBarChart extends Component {
  render () {
    return (
      <BarChart width={600} height={300} data={data}
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
  }
}

export default SimpleBarChart;
