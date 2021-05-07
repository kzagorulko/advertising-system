import React from 'react';
import {
  List,
  Datagrid,
  TextField,
  SelectField,
} from 'react-admin';
import { Empty, OneScreenListActions } from '../utils';

import primaryTypeChoices from '../../meta/BannerTypes';

const BannerTypesList = ({ onRowClick, onCreate, ...props }) => (
  <List
    title="Типы баннеров"
    empty={<Empty text="Типов баннеров не существует" hint="Создайте новый" />}
    actions={<OneScreenListActions onClick={onCreate} />}
    {...props}
  >
    <Datagrid
      rowClick={(id, basePath, record) => onRowClick && onRowClick({ id, basePath, record })}
    >
      <TextField source="id" label="Идентификатор" />
      <TextField source="name" label="Имя в системе" />
      <SelectField source="primaryType" label="Основной тип" choices={primaryTypeChoices} />
    </Datagrid>
  </List>
);

export default BannerTypesList;
