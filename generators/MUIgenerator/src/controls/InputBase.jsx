import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { InputBase } from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
    root: {
        '& .MuiTextField-root': {
            margin: theme.spacing(1),
            width: '25ch',
        },
    },
}));

export default function JDIInputBase({ type }) {
    const classes = useStyles();

    return (
        <div className={classes.root}>
            <div>
                {(type === 0) && <InputBase data-label="text-field"  required id="standard-required" defaultValue="Hello World" multiline />}
                {(type === 1) && <InputBase data-label="text-field"  disabled id="standard-disabled" defaultValue="Hello World" />}
                {(type === 2) && <InputBase data-label="text-field" 
                    id="standard-password-input"
                    type="password"
                    autoComplete="current-password"
                    defaultValue="password"
                    fullWidth
                />}
                {(type === 3) && <InputBase data-label="text-field" 
                    required
                    id="filled-required"
                    defaultValue="Hello World"
                />}
                {(type === 4) && <InputBase data-label="text-field" 
                    disabled
                    id="filled-disabled"
                    defaultValue="Hello World"
                />}
                {(type === 5) && <InputBase data-label="text-field" 
                    id="filled-number"
                    type="number"
                    defaultValue="42"
                    fullWidth
                />}
                {(type === 6) && <InputBase data-label="text-field" 
                    error
                    id="filled-error"
                    defaultValue="Hello World"
                />}
                {(type === 7) && <InputBase data-label="text-field" 
                    error
                    id="filled-error-helper-text"
                    defaultValue="Hello World"
                    multiline
                />}
            </div>
        </div>
    );
}
