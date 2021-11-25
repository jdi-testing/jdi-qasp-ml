import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Checkbox from '@material-ui/core/Checkbox';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormLabel from '@material-ui/core/FormLabel';
import FormControl from '@material-ui/core/FormControl';

const useStyles = makeStyles((theme) => ({
    root: {
        display: 'flex',
    },
    formControl: {
        margin: theme.spacing(3),
    },
}));

export const JDICheckbox = ({ basic, group, label, groupItems }) => {
    const classes = useStyles();

    const basicCheckboxes = [
        <Checkbox data-label="checkbox" 
            checked={true}
            inputProps={{ 'aria-label': 'primary checkbox' }}
        />,
        <Checkbox data-label="checkbox" 
            defaultChecked
            color="primary"
            inputProps={{ 'aria-label': 'secondary checkbox' }}
        />,
        <Checkbox data-label="checkbox"  inputProps={{ 'aria-label': 'uncontrolled-checkbox' }} />,
        <Checkbox data-label="checkbox"  disabled inputProps={{ 'aria-label': 'disabled checkbox' }} />,
        <Checkbox data-label="checkbox"  disabled checked inputProps={{ 'aria-label': 'disabled checked checkbox' }} />,
        <Checkbox data-label="checkbox" 
            defaultChecked
            indeterminate
            inputProps={{ 'aria-label': 'indeterminate checkbox' }}
        />,
        <Checkbox data-label="checkbox" 
            defaultChecked
            color="default"
            inputProps={{ 'aria-label': 'checkbox with default color' }}
        />,
        <Checkbox data-label="checkbox" 
            defaultChecked
            size="small"
            inputProps={{ 'aria-label': 'checkbox with small size' }}
        />
    ];

    const renderCheckboxLabel = (itemLabel) => (
        <FormGroup row>
            <FormControlLabel
                control={basicCheckboxes[basic.type]}
                label={itemLabel || label}
            />
        </FormGroup>
    );

    const renderGroupItem = () => {
        const render = [];
        groupItems.forEach((item, index) => {
            render.push(
                <FormControlLabel
                    key={`${item.label}${index}`}
                    control={basicCheckboxes[basic.type]}
                    label={item.label}
                />
            )
        });
        return render;
    }

    const renderCheckboxGroup = () => (
        <FormControl component="fieldset" className={classes.formControl}>
            <FormLabel component="legend">{basic.label}</FormLabel>
            <FormGroup>
                {renderGroupItem()}
            </FormGroup>
        </FormControl>
    )

    return (
        <React.Fragment>
            {
                group ? renderCheckboxGroup() : (
                    label ? renderCheckboxLabel() :
                        basicCheckboxes[basic.type]
                )
            }
        </React.Fragment>
    );
}
