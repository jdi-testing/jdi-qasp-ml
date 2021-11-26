import React from 'react';
import Backdrop from '@material-ui/core/Backdrop';
import CircularProgress from '@material-ui/core/CircularProgress';
import { makeStyles } from '@material-ui/core/styles';

export default function JDIBackdrop({open, ...rest}) {
    const useStyles = makeStyles((theme) => ({
        backdrop: {
            position: "absolute",
            zIndex: theme.zIndex.drawer + 1,
            color: '#fff',
            ...rest
        },
    }));

    const classes = useStyles();

    return (
        <div>
            <Backdrop data-label="backdrop" className={classes.backdrop} open={true} onClick={() => {}}>
                <CircularProgress data-label="progress"  color="inherit" />
            </Backdrop>
        </div>
    );
}
