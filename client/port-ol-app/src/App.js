import React, { Component } from 'react';
import logo from './alogo.png';

import _ from 'lodash'
//import SimpleBarChart from './SimpleBarChart.js';
import Chart from './components/chart';
import CountryList from './components/country_list';

// TODO have a component for each input field of the "form" to send in new data 

class App extends Component { 

  constructor(props) {
    super(props);

    this.state = {
      countrylist: [],
      selectedcountry: null,
      histogram: []
    };
    this.fetchCountryList = this.fetchCountryList.bind(this);
    this.fetchCountryList();
    this.fetchOneCountryHistogram = this.fetchOneCountryHistogram.bind(this);
    this.updateSelectedCountry = this.updateSelectedCountry.bind(this);
    this.fetchOneCountryHistogram(this.state.selectedcountry);
  }
  

  fetchCallbackHelper(url, callback) {
    fetch(url, 
       {'method': 'GET'}
       ).then(function(response) { 
        console.log("Response from fetch is " + response);
        return response.json();
    }).then(function(d) {
      callback(d);
    });

  }

  fetchCountryList() {
    this.fetchCallbackHelper('/countrydatalist', 
      (data) => {
         console.log("CL fetch: " + data.datalist);
         this.setState({
           countrylist: data.datalist,
           selectedcountry: data.datalist[0]
         });
      })
  }

  fetchOneCountryHistogram() {
    if (! this.state.selectedcountry) {
      console.log("selected country is null");
    } else {
      var ccode = this.state.selectedcountry.ccode;
      this.fetchCallbackHelper('/histogram/' + ccode, 
        (data) => {
           this.setState({
             histogram: data.data
           });
        })
    }
  }

  updateSelectedCountry(country) {
    this.setState({selectedcountry: country});
    this.fetchOneCountryHistogram();
  }

  render() {
    // magic_ lodash returns a new function here that can be run only once per 400 millisecs
    //const videoSearch = _.debounce((term) => {this.search(term)}, 400)

    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Outlier detector demo</h2>
          {this.state.selectedcountry?this.state.selectedcountry.ccode:'* *'}
        </div>
        <div className="App-intro">
          <div className="App-intro">
            <CountryList 
              onCountrySelect={this.updateSelectedCountry} 
              countrylist={this.state.countrylist} />
          </div>
          <div className="App-intro">
            <Chart data={this.state.histogram} />
          </div>
        </div>
      </div>
    );
  }
}

export default App;