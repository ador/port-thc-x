import React from 'react';


class StringField extends React.Component {

  constructor(props) {
    super(props); // needed
    if (props.defaultValue) {
      this.state = {value: props.defaultValue}
    } else {
      this.state = {value: ''}
    }
  }

  onInputChange(value) {
    this.setState({ value });
    // calling the callback, passed down from index.js
    this.props.onStringValueChange(value);
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

}

StringField.propTypes = {
  onStringValueChange: React.PropTypes.func.isRequired,
};

export default StringField;
