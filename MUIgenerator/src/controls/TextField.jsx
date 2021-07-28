import React from 'react';
import TextField from '@material-ui/core/TextField';
import { makeStyles } from '@material-ui/core/styles';

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
                {(type === 0) && <TextField required id="standard-required" label="Required" defaultValue="Hello World" />}
                {(type === 1) && <TextField disabled id="standard-disabled" label="Disabled" defaultValue="Hello World" />}
                {(type === 2) && <TextField
                    id="standard-password-input"
                    label="Password"
                    type="password"
                    autoComplete="current-password"
                />}
                {(type === 3) && <TextField
                    required
                    id="filled-required"
                    label="Required"
                    defaultValue="Hello World"
                    variant="filled"
                />}
                {(type === 4) && <TextField
                    disabled
                    id="filled-disabled"
                    label="Disabled"
                    defaultValue="Hello World"
                    variant="filled"
                />}
                {(type === 5) && <TextField
                    id="filled-number"
                    label="Number"
                    type="number"
                    InputLabelProps={{
                        shrink: true,
                    }}
                    variant="filled"
                />}
                {(type === 6) && <TextField
                    error
                    id="filled-error"
                    label="Error"
                    defaultValue="Hello World"
                    variant="filled"
                />}
                {(type === 7) && <TextField
                    error
                    id="filled-error-helper-text"
                    label="Error"
                    defaultValue="Hello World"
                    helperText="Incorrect entry."
                    variant="filled"
                />}
            </div>
        </form>
    );
}
