import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Badge from '@material-ui/core/Badge';
import MailIcon from '@material-ui/icons/Mail';
import { Typography } from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
    root: {
        '& > *': {
            margin: theme.spacing(1),
        },
    },
}));

export default function JDIBadge({ type }) {
    const classes = useStyles();

    return (
        <div className={classes.root}>
            {(type === 0) && <Badge data-label="badge" badgeContent={4} color="primary">
                <MailIcon />
            </Badge>}
            {(type === 1) && <Badge data-label="badge"  badgeContent={4} color="secondary">
                <MailIcon />
            </Badge>}
            {(type === 2) && <Badge data-label="badge" badgeContent={4} color="error">
                <MailIcon />
            </Badge>}
            {(type === 3) && <Badge data-label="badge" color="secondary" variant="dot">
                <MailIcon />
            </Badge>}
            {(type === 4) && <Badge data-label="badge" color="secondary" variant="dot">
                <Typography>Typography</Typography>
            </Badge>}
        </div>
    );
}
