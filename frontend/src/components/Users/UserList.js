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

const UserListActions = () => {
  const {
    basePath,
  } = useListContext();
  const { loaded, permissions } = usePermissions('/users');

  return loaded ? (
    <TopToolbar>
      {checkAppAction(permissions.actions, 'create') ? <CreateButton basePath={basePath} /> : null}
    </TopToolbar>
  ) : <TopToolbar />;
};

const UserList = (props) => (
  <List {...props} actions={<UserListActions />} title="Пользователи">
    <Datagrid rowClick="show">
      <TextField source="id" />
      <TextField source="displayName" />
      <TextField source="role" />
    </Datagrid>
  </List>
);

export default UserList;
