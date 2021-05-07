import React from 'react';
import {
  Create,
  TextInput,
  SelectInput,
  SimpleForm,
} from 'react-admin';
import { makeStyles } from '@material-ui/core/styles';
import styles from './style';
import { OneScreenCreateToolbar } from '../utils';
import bannerTypesChoices from '../../meta/BannerTypes';

const useStyle = makeStyles(styles);

const BannerTypesCreate = ({ onCancel, ...props }) => {
  const classes = useStyle();
  return (
    <Create component="div" classes={classes} title="Новый тип баннера" onSuccess={onCancel} {...props}>
      <SimpleForm toolbar={<OneScreenCreateToolbar onCancel={onCancel} />}>
        <TextInput source="name" label="Имя типа" />
        <SelectInput source="primaryType" label="Основной тип" choices={bannerTypesChoices} />
      </SimpleForm>
    </Create>
  );
};

export default BannerTypesCreate;
