//const {BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend} = Recharts;
import React, { Component } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';


class SimpleBarChart extends Component {

  propTypes: {
    data: React.PropTypes.array.isRequired
  }

  render () {
    return (
      <BarChart width={800} height={400} data={this.props.data}
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
