import React from 'react';
import {
  Edit,
  SimpleForm,
  TextInput,
} from 'react-admin';
import { EntityTitle } from '../utils';

const MeasureEdit = (props) => (
  <Edit title={<EntityTitle filedName="name" />} undoable={false} {...props}>
    <SimpleForm>
      <TextInput source="name" label="Название единицы измерения" />
    </SimpleForm>
  </Edit>
);

export default MeasureEdit;
