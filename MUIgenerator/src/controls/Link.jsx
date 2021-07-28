/* eslint-disable jsx-a11y/anchor-is-valid */
import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Link from '@material-ui/core/Link';
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles((theme) => ({
    root: {
        '& > * + *': {
            marginLeft: theme.spacing(2),
        },
    },
}));

export default function JDILink({ type }) {
    const classes = useStyles();
    const preventDefault = (event) => event.preventDefault();

    return (
        <Typography className={classes.root}>
            {(type === 0) && <Link href="#" onClick={preventDefault}>
                Link
            </Link>}
            {(type === 1) && <Link href="#" onClick={preventDefault} color="inherit">
                {'color="inherit"'}
            </Link>}
            {(type === 2) && <Link href="#" onClick={preventDefault} variant="body2">
                {'variant="body2"'}
            </Link>}
        </Typography>
    );
}
