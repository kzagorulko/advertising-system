import React from 'react';
import { TextInput, SelectInput } from 'react-admin';

import { OneScreenEdit } from '../utils';
import bannerTypesChoices from '../../meta/BannerTypes';

const BannerTypesEdit = ({ onCancel, record, ...props }) => (record && record.id ? (
  <OneScreenEdit onCancel={onCancel} record={record} {...props}>
    <TextInput source="name" label="Имя типа" />
    <SelectInput source="primaryType" label="Основной тип" choices={bannerTypesChoices} />
  </OneScreenEdit>
) : null);

export default BannerTypesEdit;
