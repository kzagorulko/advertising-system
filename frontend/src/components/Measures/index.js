import React from 'react';
import { OneScreenEntity } from '../utils';
import MeasureList from './MeasureList';
import MeasureCreate from './MeasureCreate';
import MeasureEdit from './MeasureEdit';

const Measures = (props) => (
  <OneScreenEntity
    List={MeasureList}
    Create={MeasureCreate}
    Edit={MeasureEdit}
    permissionName="companies"
    {...props}
  />
);

export default Measures;
