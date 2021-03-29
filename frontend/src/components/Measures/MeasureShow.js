import React from 'react';
import {
  Show,
  SimpleShowLayout,
  TextField,
} from 'react-admin';
import { EntityTitle } from '../utils';

const MeasureShow = (props) => (
  <Show title={<EntityTitle filedName="name" />} {...props}>
    <SimpleShowLayout>
      <TextField source="id" label="Идентификатор" />
      <TextField source="name" label="Название единицы измерения" />
    </SimpleShowLayout>
  </Show>
);

export default MeasureShow;
