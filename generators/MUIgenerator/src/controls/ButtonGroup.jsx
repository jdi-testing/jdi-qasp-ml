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
            {(type === 0) && <ButtonGroup data-label="button-group" color="primary" aria-label="outlined primary button group">
                <Button data-label="button" >One</Button>
                <Button data-label="button" >Two</Button>
                <Button data-label="button" >Three</Button>
            </ButtonGroup>}
            {(type === 1) && <ButtonGroup data-label="button-group" color="secondary" aria-label="outlined secondary button group">
                <Button data-label="button" >One</Button>
                <Button data-label="button" >Two</Button>
                <Button data-label="button" >Three</Button>
            </ButtonGroup>}
            {(type === 2) && <ButtonGroup data-label="button-group" size="large" color="primary" aria-label="large outlined primary button group">
                <Button data-label="button" >One</Button>
                <Button data-label="button" >Two</Button>
                <Button data-label="button" >Three</Button>
            </ButtonGroup>}
            {(type === 3) && <ButtonGroup data-label="button" Group
                orientation="vertical"
                color="primary"
                aria-label="vertical contained primary button group"
                variant="contained"
            >
                <Button data-label="button" >One</Button>
                <Button data-label="button" >Two</Button>
                <Button data-label="button" >Three</Button>
            </ButtonGroup>}
            {(type === 4) && <ButtonGroup data-label="button" Group
                orientation="vertical"
                color="primary"
                aria-label="vertical contained primary button group"
                variant="text"
            >
                <Button data-label="button" >One</Button>
                <Button data-label="button" >Two</Button>
                <Button data-label="button" >Three</Button>
            </ButtonGroup>}
            {(type === 5) && <ButtonGroup data-label="button-group" disableElevation variant="contained" color="primary">
                <Button data-label="button" >One</Button>
                <Button data-label="button" >Two</Button>
            </ButtonGroup>}
        </div>
    );
}
