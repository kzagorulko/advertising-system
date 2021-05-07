import React from 'react';
import {
  Show,
  SimpleShowLayout,
  TextField,
} from 'react-admin';
import { EntityTitle, ShowActions } from '../utils';

const MeasureShow = (props) => (
  <Show title={<EntityTitle filedName="name" />} actions={<ShowActions permissionName="measures" />} {...props}>
    <SimpleShowLayout>
      <TextField source="id" label="Идентификатор" />
      <TextField source="name" label="Название единицы измерения" />
    </SimpleShowLayout>
  </Show>
);

export default MeasureShow;
