import React from 'react';
import {
  TextInput,
} from 'react-admin';
import { OneScreenCreate } from '../utils';

const MeasureCreate = ({ onCancel, ...props }) => (
  <OneScreenCreate onCancel={onCancel} {...props}>
    <TextInput source="name" label="Название единицы измерения" />
  </OneScreenCreate>
);

export default MeasureCreate;
