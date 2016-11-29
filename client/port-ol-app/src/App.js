import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import logo from './alogo.png';
import './App.css';
import SimpleBarChart from './SimpleBarChart.js';

import Button from 'muicss/lib/react/button';
import Dropdown from 'muicss/lib/react/dropdown';
import DropdownItem from 'muicss/lib/react/dropdown-item';


class App extends Component { 

  constructor(props) {
    super(props);
    this.state = {
      countrycode : "US",
        // TODO replace this with data got from the python server (fetch)
      data : [
          {label: '10.0 - 16.2', outlier: 9, normal: 0},
          {label: '16.2 - 22.4', outlier: 5, normal: 5},
          {label: '22.4 - 28.6', outlier: 0, normal: 20},
          {label: '28.6 - 34.8', outlier: 0, normal: 50},
          {label: '34.8 - 49  .0', outlier: 0, normal: 50}
      ]
    };
    this.handleClick = this.handleClick.bind(this);
    this.getData = this.getData.bind(this);
    this.fetchAndUpdateData = this.fetchAndUpdateData.bind(this);
    this.getSelectedCountry = this.getSelectedCountry.bind(this);
    this.setSelectedCountry = this.setSelectedCountry.bind(this);
  }
  
  handleClick() {
    // TODO
  }

  getData() {
    return this.state.data;
  }

  getSelectedCountry() {
    return this.state.countrycode;
  }

  setSelectedCountry(ccode) {
    this.state.countrycode = ccode;
  }

  fetchAndUpdateData() {
    console.log("trying to fetch data from " + '/histogram/' + this.state.countrycode );
    var newdata = 
      fetch('/histogram/' + this.state.countrycode, 
         {'method': 'GET'}
         ).then(function(response) { 
          console.log("Response from fetch is " + response);
          return response.json();
      }).then(function(j) {
        console.log(j); 
      });
      this.state.data = newdata;
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
          <Dropdown color="primary" label="Dropdown" onChange={this.setSelectedCountry("CN")}>
            <DropdownItem link="#/link1">Option 1</DropdownItem>
            <DropdownItem>Option 2</DropdownItem>
            <DropdownItem>Option 3</DropdownItem>
            <DropdownItem>Option 4</DropdownItem>
          </Dropdown>
          <div>
            <Button className="mui-btn" color="primary" onClick={this.fetchAndUpdateData}>Show data</Button>
          </div>
          <div className="App-intro">
            <SimpleBarChart data={this.state.data}/>
          </div>
        </div>
      </div>
    );
  }

}

export default App;
