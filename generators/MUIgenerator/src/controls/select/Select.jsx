import React from 'react';
import JDIMultipleSelect from './Miltiselect';
import JDINativeSelects from './NativeSelect';
import JDISimpleSelect from './SimpleSelect';

export const JDISelect = ({ type, open }) => {
    return (
        <div id={`selectDiv${type[0]}`}>
            {(type[0] === 0) && <JDISimpleSelect type={type[1]} open={open} />}
            {(type[0] === 1) && <JDINativeSelects type={type[1]} open={open} />}
            {(type[0] === 2) && <JDIMultipleSelect type={type[1]} open={open} />}
        </div>
    )
}