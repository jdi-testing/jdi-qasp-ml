import React from 'react';
import PermanentDrawerLeft from './Drawer1';
import PermanentDrawerRight from './Drawer2';
import ClippedDrawer from './Drawer3';

export const JDIDrawer = ({ type }) => {
    return (
        <React.Fragment>
            {(type === 0) && <PermanentDrawerLeft />}
            {(type === 1) && <PermanentDrawerRight />}
            {(type === 2) && <ClippedDrawer />}
            
        </React.Fragment>
    )
}