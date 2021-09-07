import React from 'react';
import MiddleDividers from './grid/ChipsDividers';
import VerticalDividers from './grid/DividerButtons';
import InsetDividers from './list/insetDividers';
import SubheaderDividers from './list/subheadersDividers';
import ListDividers from './list/withDividers';

export const JDIDivider = ({type}) => {
    const lists = [
        <InsetDividers />,
        <SubheaderDividers />,
        <ListDividers />,
        <MiddleDividers />,
        <VerticalDividers />
    ];

    return (
        <React.Fragment>
            {
                lists[type]
            }
        </React.Fragment>)
}