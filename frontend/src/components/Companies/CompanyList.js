import React from 'react';
import {
  List,
  Datagrid,
  TextField,
  useListContext,
  CreateButton,
  TopToolbar,
  usePermissions,
  ReferenceField,
  DateField,
} from 'react-admin';
import { checkAppAction } from '../../utils';

const CompanyListActions = () => {
  const {
    basePath,
  } = useListContext();
  const { loaded, permissions } = usePermissions('/companies');
  return loaded ? (
    <TopToolbar>
      {checkAppAction(permissions.actions, 'create') ? <CreateButton basePath={basePath} /> : null}
    </TopToolbar>
  ) : <TopToolbar />;
};

const CompanyList = (props) => (
  <List {...props} actions={<CompanyListActions />} title="Рекламные компании">
    <Datagrid rowClick="show">
      <TextField source="id" label="Идентификатор" />
      <TextField source="title" label="Название" />
      <DateField source="startDate" label="Дата начала" />
      <DateField source="endDate" label="Дата окончания" />
      <ReferenceField link="show" label="Кто создал" source="creatorId" reference="users">
        <TextField source="displayName" />
      </ReferenceField>
    </Datagrid>
  </List>
);

export default CompanyList;
