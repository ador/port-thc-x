import React from 'react';


class StringField extends React.Component {

  constructor(props) {
    super(props); // needed

    this.state = {value: ''}
  }

  onInputChange(value) {
    this.setState({ value });
    console.log("from stringfield " + value);
    // calling the callback, passed down from index.js
    this.props.onStringValueChange(value);
  }

  render() {
    return (
      <div className="myfield">
      <input
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
