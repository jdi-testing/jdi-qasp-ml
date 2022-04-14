import React from 'react';
import TextField from '@material-ui/core/TextField';
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

export default function JDITextField({ type }) {
    const classes = useStyles();

    return (
        <form className={classes.root} noValidate autoComplete="off">
            <div>
                {(type === 0) && <TextField data-label="text-field" required id="standard-required" label="Required" defaultValue="Hello World" />}
                {(type === 1) && <TextField data-label="text-field" disabled id="standard-disabled" label="Disabled" defaultValue="Hello World" fullWidth />}
                {(type === 2) && <TextField data-label="text-field"
                    id="standard-password-input"
                    label="Password"
                    type="password"
                    autoComplete="current-password"
                />}
                {(type === 3) && <TextField data-label="text-field"
                    required
                    id="filled-required"
                    label="Required"
                    defaultValue="Hello World"
                    variant="filled"
                />}
                {(type === 4) && <TextField data-label="text-field"
                    disabled
                    id="filled-disabled"
                    label="Disabled"
                    defaultValue="Hello World"
                    variant="filled"
                    multiline
                />}
                {(type === 5) && <TextField data-label="text-field"
                    id="filled-number"
                    label="Number"
                    type="number"
                    InputLabelProps={{
                        shrink: true,
                    }}
                    variant="filled"
                />}
                {(type === 6) && <TextField data-label="text-field"
                    error
                    id="filled-error"
                    label="Error"
                    defaultValue="Hello World"
                    variant="filled"
                    multiline
                />}
                {(type === 7) && <TextField data-label="text-field"
                    error
                    id="filled-error-helper-text"
                    label="Error"
                    defaultValue="Hello World"
                    helperText="Incorrect entry."
                    variant="filled"
                    fullWidth
                />}
            </div>
        </form>
    );
}
