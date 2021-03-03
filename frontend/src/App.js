import React from 'react';
import { Admin, Resource } from 'react-admin';
import dataProvider from './api/dataProvider';
import authProvider from './api/authProvider';
import UserList from './components/Users/UserList';
import UserShow from './components/Users/UserShow';
import UserCreate from './components/Users/UserCreate';
import UserEdit from './components/Users/UserEdit';

import './App.less';

import { checkAppAction } from './utils';

const App = () => (
  <Admin title="Flower System" dataProvider={dataProvider} authProvider={authProvider}>
    {(permissions) => [
      permissions.users
        ? (
          <Resource
            name="users"
            list={UserList}
            show={UserShow}
            create={checkAppAction(permissions.users, 'create') ? UserCreate : null}
            edit={checkAppAction(permissions.users, 'update') ? UserEdit : null}
            options={{ label: 'Пользователи' }}
          />
        ) : null,
    ]}
  </Admin>
);

export default App;
