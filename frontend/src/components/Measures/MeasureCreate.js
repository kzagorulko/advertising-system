import React from 'react';
import {
  SimpleForm,
  Create,
  TextInput,
} from 'react-admin';

const MeasureCreate = (props) => (
  <Create title="Новая единица измерения" {...props}>
    <SimpleForm>
      <TextInput source="name" label="Название единицы измерения" />
    </SimpleForm>
  </Create>
);

export default MeasureCreate;
