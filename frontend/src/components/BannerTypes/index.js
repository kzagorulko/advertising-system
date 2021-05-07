import React from 'react';
import BannerTypesList from './BannerTypesList';
import BannerTypesCreate from './BannerTypesCreate';
import BannerTypesEdit from './BannerTypesEdit';
import { OneScreenList } from '../utils';

const BannerTypes = (props) => (
  <OneScreenList
    List={BannerTypesList}
    Create={BannerTypesCreate}
    Edit={BannerTypesEdit}
    // permissionName="banner_types"
    {...props}
  />
);

export default BannerTypes;
