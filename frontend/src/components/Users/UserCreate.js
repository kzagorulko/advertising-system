import React from 'react';
import {
  SimpleForm,
  Create,
  TextInput,
} from 'react-admin';

const UserCreate = (props) => (
  <Create title="Новый пользователь" {...props}>
    <SimpleForm>
      <TextInput source="username" />
      <TextInput source="password" />
      <TextInput source="displayName" />
      <TextInput source="email" />
      <TextInput source="role" />
    </SimpleForm>
  </Create>
);

export default UserCreate;
