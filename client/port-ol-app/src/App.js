import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import SimpleBarChart from './SimpleBarChart.js';


class App extends Component {
  //propTypes: {
  //  data: React.PropTypes.array.isRequired
  //},

  render() {
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Welcome to React</h2>
        </div>
        <p className="App-intro">
          Hello, world
         </p>
         <SimpleBarChart />

        
      </div>
    );
  }
}

export default App;
