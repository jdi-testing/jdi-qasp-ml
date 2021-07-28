import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Popper from '@material-ui/core/Popper';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';

const useStyles = makeStyles((theme) => ({
    root: {
        width: 500,
    },
    typography: {
        padding: theme.spacing(2),
    },
    paper: {
        border: '1px solid',
        padding: theme.spacing(1),
        backgroundColor: theme.palette.background.paper,
      },
}));

export default function JDIPopper({ type }) {
    const classes = useStyles();

    return (
        <div id="popperContainer" className={classes.root}>
            {(type === 0) && <Popper open anchorEl={document.getElementById("popperContainer")} placement="bottom-end" transition>
                <Paper>
                    <Typography className={classes.typography}>The content of the Popper.</Typography>
                </Paper>
            </Popper>}
            {(type === 1) && <Popper open={true} anchorEl={document.getElementById("popperContainer")} placement="left-end">
                <div className={classes.paper}>The content of the Popper.</div>
            </Popper>}
        </div>
    );
}