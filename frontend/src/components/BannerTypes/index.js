import React from 'react';
import BannerTypesList from './BannerTypesList';
import BannerTypesCreate from './BannerTypesCreate';
import BannerTypesEdit from './BannerTypesEdit';
import { OneScreenEntity } from '../utils';

const BannerTypes = (props) => (
  <OneScreenEntity
    List={BannerTypesList}
    Create={BannerTypesCreate}
    Edit={BannerTypesEdit}
    {...props}
  />
);

export default BannerTypes;
