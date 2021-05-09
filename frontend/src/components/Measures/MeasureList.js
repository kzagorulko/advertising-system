import React from 'react';
import {
  TextField,
} from 'react-admin';
import { Empty, OneScreenList } from '../utils';

const MeasureList = ({ onCreate, onRowClick, ...props }) => (
  <OneScreenList
    onCreate={onCreate}
    title="Единицы измерения"
    onRowClick={onRowClick}
    empty={<Empty text="Единиц измерений не существует" hint="Создайте новую" />}
    {...props}
  >
    <TextField source="id" label="Идентификатор" />
    <TextField source="name" label="Название единицы измерения" />
  </OneScreenList>
);

export default MeasureList;
