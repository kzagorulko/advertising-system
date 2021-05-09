import React from 'react';
import {
  TextField,
  SelectField,
} from 'react-admin';
import { Empty, OneScreenList } from '../utils';

import primaryTypeChoices from '../../meta/BannerTypes';

const BannerTypesList = ({ onRowClick, onCreate, ...props }) => (
  <OneScreenList
    onRowClick={onRowClick}
    empty={<Empty text="Типов баннеров не существует" hint="Создайте новый" />}
    title="Типы баннеров"
    onCreate={onCreate}
    {...props}
  >
    <TextField source="id" label="Идентификатор" />
    <TextField source="name" label="Имя в системе" />
    <SelectField source="primaryType" label="Основной тип" choices={primaryTypeChoices} />
  </OneScreenList>
);

export default BannerTypesList;
