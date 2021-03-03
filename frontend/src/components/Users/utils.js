import React from 'react';

const UserTitle = ({ record }) => (
  <span>{record ? record.displayName : ''}</span>
);

export default UserTitle;
