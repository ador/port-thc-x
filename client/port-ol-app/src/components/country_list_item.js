import React from 'react';

const CountryListItem = ({country, onCountrySelect}) => {

  const ccode = country.ccode;
  const outliers = country.outlier_num;
  const normals = country.normal_num;
  const total = outliers + normals;

  return (
    <li onClick={() => onCountrySelect(country)}
    className="list-group-item">
      <div className="video-list media">
        <h3> {ccode} </h3>
      </div>
      <div>
        <p> Total data points:  {total} </p>
        <p> Outliers:  {outliers} </p>
      </div>
    </li>
  );
};

export default CountryListItem;
