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
      histogram: [],
      // form field values
      idVal: 0,
      portcodeVal: "",
      currencyVal: "USD",
      valueVal: "0.0"
    };
    this.fetchCountryList = this.fetchCountryList.bind(this);
    this.fetchOneCountryHistogram = this.fetchOneCountryHistogram.bind(this);
    this.updateSelectedCountry = this.updateSelectedCountry.bind(this);
    this.updateIdVal = this.updateIdVal.bind(this);
    this.updatePortcodeVal = this.updatePortcodeVal.bind(this);
    this.updateCurrencyVal = this.updateCurrencyVal.bind(this);
    this.updateValueVal = this.updateValueVal.bind(this);
    this.getCheckedFormData = this.getCheckedFormData.bind(this);
    this.sendData = this.sendData.bind(this);
    this.fetchCountryList();
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
    this.setState({selectedcountry: country});
    // react picks the setState up a bit later, so
    // do not use the state in this call, but the param
    this.fetchOneCountryHistogram(country);
  }

  updateIdVal(value) {
    this.setState({idVal: parseInt(value)})
  }

  updatePortcodeVal(value) {
    this.setState({portcodeVal: value.toUpperCase()})
  }

  updateCurrencyVal(value) {
    this.setState({currencyVal: value.toUpperCase()})
  }

  updateValueVal(value) {
    this.setState({valueVal: parseFloat(value)})
  }

  getCheckedFormData() {
    // TODO : check and fix form data if possible
    var data = {
      "currency": this.state.currencyVal,
      "value": parseFloat(this.state.valueVal),
      "port": this.state.portcodeVal, 
      "supplier_id": parseInt(this.state.idVal)
    }
    return data;
  }

  sendData() {
    var toSend = this.getCheckedFormData();
    console.log("now we should send data:");
    console.log(toSend);
    var that = this;
    fetch("/upload",
    {
        headers: {
          'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify(toSend)
    })
    .then(function(res){ 
      console.log(res)
      // refresh country data with the new
      that.fetchCountryList();
    }).catch(function(res){ console.log(res) })
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
        <div className="row"> 
          <div className="col-sm-3 ">
            <DataForm 
                  onIdChange={this.updateIdVal}
                  onPortChange={this.updatePortcodeVal}
                  onValChange={this.updateValueVal}
                  onCurrChange={this.updateCurrencyVal}
                  onSubmitClick={this.sendData} />
          </div>
        </div>
      </div>
    );
  }
}

export default App;