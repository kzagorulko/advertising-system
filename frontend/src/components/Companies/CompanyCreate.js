import React from 'react';
import {
  SimpleForm,
  Create,
  TextInput,
  ReferenceInput,
  AutocompleteInput,
  DateInput,
  NumberInput,
} from 'react-admin';

const CompanyCreate = (props) => (
  <Create title="Новая рекламная компания" {...props}>
    <SimpleForm>
      <TextInput source="title" label="Название" />
      <DateInput source="startDate" label="Дата начала" />
      <DateInput source="endDate" label="Дата окончания" />
      <NumberInput source="exceptedProfit" label="Ожидаемый профит" />
      <ReferenceInput source="measureId" reference="measures" label="Единица измерения">
        <AutocompleteInput optionText="name" />
      </ReferenceInput>
    </SimpleForm>
  </Create>
);

export default CompanyCreate;
