import React from 'react';
import {
  Show,
  SimpleShowLayout,
  TextField,
  ReferenceField,
  DateField,
  NumberField,
} from 'react-admin';
import { EntityTitle, ShowActions } from '../utils';

const CompanyShow = (props) => (
  <Show title={<EntityTitle filedName="title" />} actions={<ShowActions permissionName="companies" />} {...props}>
    <SimpleShowLayout>
      <TextField source="id" label="Идентификатор" />
      <TextField source="title" label="Название" />
      <DateField source="startDate" label="Дата начала" />
      <DateField source="endDate" label="Дата оконнчания" />
      <NumberField source="exceptedProfit" label="Ожидаемый профит" />
      <NumberField source="profit" label="Итогоый профит" />
      <ReferenceField link="show" label="Единица измерения" source="measureId" reference="measures">
        <TextField source="name" />
      </ReferenceField>
      <ReferenceField link="show" label="Кто создал" source="creatorId" reference="users">
        <TextField source="displayName" />
      </ReferenceField>
    </SimpleShowLayout>
  </Show>
);

export default CompanyShow;
