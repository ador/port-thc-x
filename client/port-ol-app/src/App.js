import React, { Component } from 'react';
import logo from './alogo.png';

import Chart from './components/chart';
import CountryList from './components/country_list';
import DataForm from './components/data_form'

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
    return fetch(url, 
       {'method': 'GET'}
    ).then(function(response) { 
          return response.json();
      })
  }

  fetchCountryList() {
    this.fetchCallbackHelper('/countrydatalist')
    .then(data => {
         this.setState({
           countrylist: data.datalist,
           selectedcountry: data.datalist[0]
         });
      })
  }

  fetchOneCountryHistogram(country) {
    if (! country) {
      console.log("selected country is null");
    } else {
      var ccode = country.ccode;
      this.fetchCallbackHelper('/histogram/' + ccode)
      .then(data => {
           this.setState({
             histogram: data.data
           });
      })
    }
  }

  updateSelectedCountry(country) {
    // react picks the setstate up later
    this.setState({selectedcountry: country});
    this.fetchOneCountryHistogram(country);
  }

  logIt(something) {
    console.log(something);
  }

  render() {

    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Outlier detector demo</h2>
        </div>
        <div className="row">
          <div className="col-sm-3">
            <CountryList 
              onCountrySelect={this.updateSelectedCountry} 
              countrylist={this.state.countrylist} />
          </div>
          <div className="col-sm-9 histo ">
            <Chart data={this.state.histogram} />
          </div>
        </div>
        <div> 
          <DataForm 
                onIdChange={this.logIt}
                onPortChange={this.logIt}
                onValChange={this.logIt}
                onCurrChange={this.logIt} />
        </div>
      </div>
    );
  }
}

export default App;