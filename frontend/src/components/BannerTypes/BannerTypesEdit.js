import React from 'react';
import {
  SimpleForm,
  Edit,
  TextInput,
  SelectInput,
} from 'react-admin';
import { makeStyles } from '@material-ui/core/styles';

import { OneScreenCreateToolbar } from '../utils';
import bannerTypesChoices from '../../meta/BannerTypes';
import styles from './style';

const useStyle = makeStyles(styles);

const BannerTypesEdit = ({ onCancel, record, ...props }) => {
  const classes = useStyle();
  return (record && record.id ? (
    <Edit title=" " onSuccess={onCancel} undoable={false} {...props} id={record.id} classes={classes}>
      <SimpleForm toolbar={<OneScreenCreateToolbar onCancel={onCancel} />}>
        <TextInput source="name" label="Имя типа" />
        <SelectInput source="primaryType" label="Основной тип" choices={bannerTypesChoices} />
      </SimpleForm>
    </Edit>
  ) : null);
};

export default BannerTypesEdit;
