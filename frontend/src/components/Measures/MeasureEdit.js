import React from 'react';
import {
  TextInput,
} from 'react-admin';
import { OneScreenEdit } from '../utils';

const MeasureEdit = ({ onCancel, record, ...props }) => (record && record.id ? (
  <OneScreenEdit record={record} onCancel={onCancel} {...props}>
    <TextInput source="name" label="Название единицы измерения" />
  </OneScreenEdit>
) : null);

export default MeasureEdit;
