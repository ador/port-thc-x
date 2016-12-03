import React from 'react';
import NumberField from './number_field';
import StringField from './string_field';


class DataForm extends React.Component {

  constructor(props) {
    super(props); // needed 
    //this.state = {value: '0'}
  }

  render() {
    return (
        <ul className="list-group">
          <li> Supplier ID: <NumberField onNumberValueChange={this.props.onIdChange}/> </li>
          <li> Port code: <StringField onStringValueChange={this.props.onPortChange}/> </li>
          <li> Currency: <StringField onStringValueChange={this.props.onValChange}/> </li>
          <li> Value: <NumberField onNumberValueChange={this.props.onCurrChange}/> </li>
        </ul>
    );
  }
};

DataForm.propTypes = {
  onIdChange: React.PropTypes.func.isRequired,
  onPortChange: React.PropTypes.func.isRequired,
  onValChange: React.PropTypes.func.isRequired,
  onCurrChange: React.PropTypes.func.isRequired,
};

export default DataForm

