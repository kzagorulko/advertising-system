import React from 'react';
import { TextInput, SelectInput } from 'react-admin';
import { OneScreenCreate } from '../utils';
import bannerTypesChoices from '../../meta/BannerTypes';

const BannerTypesCreate = ({ onCancel, ...props }) => (
  <OneScreenCreate onCancel={onCancel} {...props}>
    <TextInput source="name" label="Имя типа" />
    <SelectInput source="primaryType" label="Основной тип" choices={bannerTypesChoices} />
  </OneScreenCreate>
);

export default BannerTypesCreate;
