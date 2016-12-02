import React from 'react';
import CountryListItem from './country_list_item';

const CountryList = (props) => {
  console.log('render called', props);
  if (!props.countrylist) {
    return <div> Waiting... </div>;
  }

  const countryListItems = props.countrylist.map((elem) => {
    return <CountryListItem
      key={elem.ccode}
      country={elem}
      onCountrySelect={props.onCountrySelect} />
  });

  return (
      <ul className="col-md-4 list-group">
        {countryListItems}
      </ul>
  );
};

CountryList.propTypes = {
  countrylist: React.PropTypes.array.isRequired,
};

export default CountryList