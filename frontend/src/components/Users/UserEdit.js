import React from 'react';
import {
  Edit,
  SimpleForm,
  TextInput,
  BooleanInput,
} from 'react-admin';
import UserTitle from './utils';

const UserEdit = (props) => (
  <Edit title={<UserTitle />} undoable={false} {...props}>
    <SimpleForm>
      <TextInput disabled source="id" />
      <TextInput disabled source="username" />
      <TextInput source="displayName" />
      <TextInput source="password" />
      <BooleanInput source="deactivated" />
      <TextInput source="role" />
    </SimpleForm>
  </Edit>
);

export default UserEdit;
