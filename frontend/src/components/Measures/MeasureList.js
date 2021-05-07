import React from 'react';
import {
  List,
  Datagrid,
  TextField,
  useListContext,
  CreateButton,
  TopToolbar,
  usePermissions,
} from 'react-admin';
import { checkAppAction } from '../../utils';

const MeasureListActions = () => {
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

const MeasureList = (props) => (
  <List {...props} actions={<MeasureListActions />} title="Единицы измерения">
    <Datagrid rowClick="show">
      <TextField source="id" label="Идентификатор" />
      <TextField source="name" label="Название единицы измерения" />
    </Datagrid>
  </List>
);

export default MeasureList;
