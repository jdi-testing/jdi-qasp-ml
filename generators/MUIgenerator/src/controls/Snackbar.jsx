import React from 'react';
import Snackbar from '@material-ui/core/Snackbar';
import { makeStyles } from '@material-ui/core/styles';
import { IconButton } from '@material-ui/core';
import CloseIcon from '@material-ui/icons/Close';
const useStyles = makeStyles((theme) => ({
    root: {
        width: '100%',
        '& > * + *': {
            marginTop: theme.spacing(2),
        },
    },
}));

export default function JDISnackbar({ type, text }) {
    const classes = useStyles();

    const handleClose = () => {
    };

    return (
        <div className={classes.root}>
            <Snackbar data-label="snackbar" open onClose={handleClose} message={text} action={
                <IconButton data-label="button" size="small" aria-label="close" color="inherit" onClick={handleClose}>
                    <CloseIcon data-label="icon" fontSize="small" />
                </IconButton>
            }>
            </Snackbar>
        </div>
    );
}
