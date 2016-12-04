import React, { Component } from 'react';
import logo from './alogo.png';

import Chart from './components/chart';
import CountryList from './components/country_list';
import DataForm from './components/data_form';
import Alert from 'react-s-alert';
import 'react-s-alert/dist/s-alert-default.css';
import 'react-s-alert/dist/s-alert-css-effects/slide.css';

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
      valueVal: 0.0
    };

    // binding functions
    this.fetchCountryList = this.fetchCountryList.bind(this);
    this.fetchOneCountryHistogram = this.fetchOneCountryHistogram.bind(this);
    this.updateSelectedCountry = this.updateSelectedCountry.bind(this);
    this.updateIdVal = this.updateIdVal.bind(this);
    this.updatePortcodeVal = this.updatePortcodeVal.bind(this);
    this.updateCurrencyVal = this.updateCurrencyVal.bind(this);
    this.updateValueVal = this.updateValueVal.bind(this);
    this.getCheckedFormData = this.getCheckedFormData.bind(this);
    this.alertError = this.alertError.bind(this);
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
    this.fetchOneCountryHistogram(country);
  }

  updateIdVal(value) {
    this.setState({idVal: parseInt(value, 10)})
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

  alertError(msg){
    Alert.error(msg, {
          position: 'bottom-left',
          effect: 'slide',
          timeout: 3000
        });
  }

  checkValue(val) {
    if (!val) {
      this.alertError('Please fill Value (number)');
      return false;
    } else {
      if (typeof val !== "number" || val < 0) {
        this.alertError('Value must be a positive number');
        return false;
      }
    }
    return true;
  }

  checkCurrency(currency) {
    if (!currency) {
      this.alertError('Please fill Currency (3-letter code)');
      return false;
    }
    if (!currency.match(/^[A-Z][A-Z][A-Z]$/)) {
      this.alertError('Currency must be a 3-letter string containing just letters A-Z');
      return false;
    }
    return true;
  }

  checkPortcode(portcode) {
    if (!portcode) {
      this.alertError('Please fill Port code (5-letter code)');
      return false;
    }
    if (!portcode.match(/^[A-Z][A-Z][A-Z][A-Z][A-Z]$/)) {
      this.alertError('Port code must be a 5-letter string containing just letters A-Z');
      return false;
    }
    return true;
  }

  checkId(id) {
    if (!id) {
      this.alertError('Please fill Supplier ID code (integer)');
      return false;
    }
    if (id < 0) {
      this.alertError('Supplier ID must be a positive integer');
      return false;
    }
    return true;
  }


  getCheckedFormData() {
    // TODO: more scrict checks
    //console.log("checkformdata")
    if (this.checkCurrency(this.state.currencyVal) && 
        this.checkValue(this.state.valueVal) &&
        this.checkPortcode(this.state.portcodeVal) &&
        this.checkId(this.state.idVal)) {
      var data = {
        "currency": this.state.currencyVal,
        "value": parseFloat(this.state.valueVal),
        "port": this.state.portcodeVal, 
        "supplier_id": parseInt(this.state.idVal, 10)
      }
      return data;
    } else {
     return null;
    }
  }

  sendData() {
    var toSend = this.getCheckedFormData();
    if (toSend) {
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
        if (res.ok) {
          Alert.success('Data has been received by the server', {
            position: 'bottom-left',
            effect: 'slide',
            timeout: 1500
          });
          // refresh country data with the new
          that.fetchCountryList();
        } else {
          Alert.error('The server could not accept the data', {
            position: 'bottom-left',
            effect: 'slide',
            timeout: 2000
          });
        }
      }).catch(function(res){ console.log(res) })
    }
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
                  defaultCurrency={this.state.currencyVal}
                  onSubmitClick={this.sendData} />
          </div>
        </div>
        <Alert stack={{limit: 3}} />
      </div>
    );
  }
}

export default App;