import React from 'react';

const CountryListItem = ({country, onCountrySelect}) => {

  const ccode = country.ccode;
  const outliers = country.outlier_num;
  const normals = country.normal_num;
  const total = outliers + normals;

  return (
    <li onClick={() => onCountrySelect(country)}
    className="list-group-item">
      <div className="country-item ">
        <h4> {ccode} </h4>
        Total data points:  {total} <br />
        Outliers:  {outliers}
      </div>
    </li>
  );
};

export default CountryListItem;
