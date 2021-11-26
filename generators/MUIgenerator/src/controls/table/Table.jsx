import React from 'react';
import BasicTable from './Basic';
import CollapsibleTable from './Collapsible';
import CustomizedTables from './Customized';
import DataTable from './DataTable';
import DenseTable from './DenseTable';
import EnhancedTable from './SortingTable';

export const JDITable = ({type}) => {
    const tables = [
        <BasicTable />,
        <CollapsibleTable />,
        <CustomizedTables />,
        <DataTable />,
        <DenseTable />,
        <EnhancedTable />,
    ];

    return (
        <React.Fragment>
            {
                tables[type]
            }
        </React.Fragment>)
}