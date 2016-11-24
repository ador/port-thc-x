import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import logo from './alogo.png';
import './App.css';
import SimpleBarChart from './SimpleBarChart.js';

import Button from 'muicss/lib/react/button';
import Dropdown from 'muicss/lib/react/dropdown';
import DropdownItem from 'muicss/lib/react/dropdown-item';


class App extends Component {
  countrycode = "US"

  // TODO replace this with data got from the python server (fetch)
  data = [
      {label: '10.0 - 16.2', outlier: 9, normal: 0},
      {label: '16.2 - 22.4', outlier: 5, normal: 5},
      {label: '22.4 - 28.6', outlier: 0, normal: 20},
      {label: '28.6 - 34.8', outlier: 0, normal: 50},
      {label: '34.8 - 49  .0', outlier: 0, normal: 50}
  ]


  getSelectedCountry() {
    return "CN"
  }

  render() {
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Outlier detector demo</h2>
        </div>
        <div className="App-intro">
          Choose countrycode! 
          <Dropdown color="primary" label="Dropdown" onChange={this.log()}>
            <DropdownItem link="#/link1">Option 1</DropdownItem>
            <DropdownItem>Option 2</DropdownItem>
            <DropdownItem>Option 3</DropdownItem>
            <DropdownItem>Option 4</DropdownItem>
          </Dropdown>
          <div>
            <Button className="mui-btn" color="primary" onClick={(event)=>this.log(event)}>Show data</Button>
          </div>
          <div className="App-intro">
            <SimpleBarChart data={this.data}/>
          </div>
        </div>
      </div>
    );
  }

  log(event) {
      console.log("something should change here!")
  }

}

export default App;
