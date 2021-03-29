import React from 'react';
import {
  Edit,
  SimpleForm,
  TextInput,
  ReferenceInput,
  AutocompleteInput,
  DateInput,
  NumberInput,
} from 'react-admin';
import { EntityTitle } from '../utils';

const CompanyEdit = (props) => (
  <Edit title={<EntityTitle filedName="title" />} undoable={false} {...props}>
    <SimpleForm>
      <TextInput disabled source="id" label="Идентификатор" />
      <TextInput source="title" label="Название" />
      <DateInput source="startDate" label="Дата начала" />
      <DateInput source="endDate" label="Дата окончания" />
      <NumberInput disabled source="exceptedProfit" label="Ожидаемая прибль" />
      <NumberInput source="profit" label="Итоговая прибль" />
      <ReferenceInput source="measureId" reference="measures" label="Единица измерения">
        <AutocompleteInput optionText="name" />
      </ReferenceInput>
    </SimpleForm>
  </Edit>
);

export default CompanyEdit;
