import React from 'react';
import MiddleDividers from './ChipsDividers';
import VerticalDividers from './DividerButtons';


export const JDIGrid = ({type}) => {
    const components = [
        <MiddleDividers />,
        <VerticalDividers />
    ];

    return (
        <React.Fragment>
            {
                components[type]
            }
        </React.Fragment>)
}