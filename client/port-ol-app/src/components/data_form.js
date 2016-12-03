import React from 'react';
import NumberField from './number_field';
import StringField from './string_field';


class DataForm extends React.Component {

  render() {
    return (
        <div className="submitform">
        <h3> Submit new data </h3>
        <ul className="list-group">
          <li> Supplier ID: <NumberField onNumberValueChange={this.props.onIdChange}/> </li>
          <li> Port code: <StringField onStringValueChange={this.props.onPortChange}/> </li>
          <li> Currency: <StringField onStringValueChange={this.props.onCurrChange}/> </li>
          <li> Value: <NumberField onNumberValueChange={this.props.onValChange}/> </li>
          <li onClick={() => this.props.onSubmitClick()} 
              className="myfield list-group-item submit"> SUBMIT </li>
        </ul>
        </div>
    );
  }
};

DataForm.propTypes = {
  onIdChange: React.PropTypes.func.isRequired,
  onPortChange: React.PropTypes.func.isRequired,
  onValChange: React.PropTypes.func.isRequired,
  onCurrChange: React.PropTypes.func.isRequired,
  onSubmitClick: React.PropTypes.func.isRequired
};

export default DataForm

