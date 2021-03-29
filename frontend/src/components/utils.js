import React from 'react';
import {
  CreateButton,
  EditButton,
  TopToolbar,
  usePermissions,
  ListButton,
  ShowButton,
} from 'react-admin';

import { checkAppAction } from '../utils';

export const EntityTitle = ({ filedName, record }) => (
  <span>{record ? record[filedName] : ''}</span>
);

export const ListActions = ({ basePath, permissionName }) => {
  const { loaded, permissions } = usePermissions(`/${permissionName}`);

  return loaded ? (
    <TopToolbar>
      {checkAppAction(permissions.actions, 'create') ? <CreateButton basePath={basePath} label="Создать" /> : null}
    </TopToolbar>
  ) : <TopToolbar />;
};

export const ShowActions = ({ basePath, permissionName, data }) => {
  const { loaded, permissions } = usePermissions(`/${permissionName}`);

  return loaded ? (
    <TopToolbar>
      <ListButton basePath={basePath} label="Список" />
      {checkAppAction(permissions.actions, 'update')
        ? <EditButton basePath={basePath} label="Редактировать" record={data} /> : null}
    </TopToolbar>
  ) : <TopToolbar />;
};

export const EditActions = ({ basePath, data }) => (
  <TopToolbar>
    <ListButton basePath={basePath} label="Список" />
    <ShowButton basePath={basePath} label="Просмотр" record={data} />
  </TopToolbar>
);
