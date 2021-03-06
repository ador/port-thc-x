import React from 'react';


class NumberField extends React.Component {

  constructor(props) {
    super(props); // needed 
    this.state = {value: '0'}
  }

  onInputChange(value) {
    this.setState({ value });
    // calling the callback, passed down from index.js
    this.props.onNumberValueChange(value);
  }

  render() {
    return (
      <div className="myfield">
      <input className="form-control input-md"
        value={this.state.value}
        onChange={(e) => this.onInputChange(e.target.value)} />
      </div>
    );
  }

};

NumberField.propTypes = {
  onNumberValueChange: React.PropTypes.func.isRequired,
};

export default NumberField;
