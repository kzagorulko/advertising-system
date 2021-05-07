import React from 'react';
import { Admin, Resource } from 'react-admin';
import polyglotI18nProvider from 'ra-i18n-polyglot';
import russianMessages from 'ra-language-russian';
import dataProvider from './api/dataProvider';
import authProvider from './api/authProvider';

import './App.less';

import { checkAppAction } from './utils';
import UserList from './components/Users/UserList';
import UserShow from './components/Users/UserShow';
import UserCreate from './components/Users/UserCreate';
import UserEdit from './components/Users/UserEdit';
import RoleList from './components/Roles/RoleList';
import RoleShow from './components/Roles/RoleShow';
import MeasureList from './components/Measures/MeasureList';
import CompanyList from './components/Companies/CompanyList';
import MeasureCreate from './components/Measures/MeasureCreate';
import MeasureShow from './components/Measures/MeasureShow';
import MeasureEdit from './components/Measures/MeasureEdit';
import CompanyCreate from './components/Companies/CompanyCreate';
import CompanyShow from './components/Companies/CompanyShow';
import CompanyEdit from './components/Companies/CompanyEdit';
import BannerTypes from './components/BannerTypes';

const i18nProvider = polyglotI18nProvider(() => russianMessages, 'ru');

const App = () => (
  <Admin title="Flower System" dataProvider={dataProvider} authProvider={authProvider} i18nProvider={i18nProvider}>
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
      permissions.users
        ? (
          <Resource
            name="roles"
            list={RoleList}
            options={{ label: 'Роли' }}
            show={RoleShow}
          />
        ) : null,
      permissions.companies
        ? (
          <Resource
            name="measures"
            list={MeasureList}
            options={{ label: 'Меры' }}
            create={MeasureCreate}
            show={MeasureShow}
            edit={MeasureEdit}
          />
        ) : null,
      permissions.companies
        ? (
          <Resource
            name="companies"
            list={CompanyList}
            options={{ label: 'Рекламные компании' }}
            create={CompanyCreate}
            show={CompanyShow}
            edit={CompanyEdit}
          />
        ) : null,
      permissions.banner_types
        ? (
          <Resource
            name="bannerTypes"
            list={BannerTypes}
            options={{ label: 'Типы банеров' }}
          />
        ) : null,
    ]}
  </Admin>
);

export default App;
