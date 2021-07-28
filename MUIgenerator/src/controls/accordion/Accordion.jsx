import React from 'react';
import ControlledAccordions from './ControlledAccordion';
import CustomizedAccordions from './CustomizedAcordion';
import SimpleAccordion from './SimpleAccordion';

export const JDIAccordeon = ({ type }) => {
    return (
        <React.Fragment>
            {(type === 0) && <SimpleAccordion />}
            {(type === 1) && <ControlledAccordions />}
            {(type === 2) && <CustomizedAccordions />}

        </React.Fragment>
    )
}