import React from 'react';
import InsetDividers from './insetDividers';
import SubheaderDividers from './subheadersDividers';
import ListDividers from './withDividers';

export const JDIList = ({type}) => {
    const lists = [
        <InsetDividers />,
        <SubheaderDividers />,
        <ListDividers />
    ];

    return (
        <React.Fragment>
            {
                lists[type]
            }
        </React.Fragment>)
}