import React from 'react';
import Button from '@material-ui/core/Button';
import ButtonGroup from '@material-ui/core/ButtonGroup';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
    root: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        '& > *': {
            margin: theme.spacing(1),
        },
    },
}));

export default function JDIButtonGroup({type}) {
    const classes = useStyles();

    return (
        <div className={classes.root}>
            {(type === 0) && <ButtonGroup color="primary" aria-label="outlined primary button group">
                <Button>One</Button>
                <Button>Two</Button>
                <Button>Three</Button>
            </ButtonGroup>}
            {(type === 1) && <ButtonGroup color="secondary" aria-label="outlined secondary button group">
                <Button>One</Button>
                <Button>Two</Button>
                <Button>Three</Button>
            </ButtonGroup>}
            {(type === 2) && <ButtonGroup size="large" color="primary" aria-label="large outlined primary button group">
                <Button>One</Button>
                <Button>Two</Button>
                <Button>Three</Button>
            </ButtonGroup>}
            {(type === 3) && <ButtonGroup
                orientation="vertical"
                color="primary"
                aria-label="vertical contained primary button group"
                variant="contained"
            >
                <Button>One</Button>
                <Button>Two</Button>
                <Button>Three</Button>
            </ButtonGroup>}
            {(type === 4) && <ButtonGroup
                orientation="vertical"
                color="primary"
                aria-label="vertical contained primary button group"
                variant="text"
            >
                <Button>One</Button>
                <Button>Two</Button>
                <Button>Three</Button>
            </ButtonGroup>}
            {(type === 5) && <ButtonGroup disableElevation variant="contained" color="primary">
                <Button>One</Button>
                <Button>Two</Button>
            </ButtonGroup>}
        </div>
    );
}
