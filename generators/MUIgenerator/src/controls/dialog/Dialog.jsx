import React from 'react';
import AlertDialog from './alertDialog';
import ConfirmationDialog from './confirmation';
import CustomizedDialogs from './customizedDialog';
import FormDialog from './formDialog';
import MaxWidthDialog from './optionalSize';


export const JDIDialog = ({type}) => {
    const components = [
        <AlertDialog />,
        <ConfirmationDialog />,
        <CustomizedDialogs />,
        <FormDialog />,
        <MaxWidthDialog />
    ];

    return (
        <div id="modalDivsContainer">
            {
                components[type]
            }
        </div>)
}