import React from 'react';
import Popover from '@material-ui/core/Popover';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
    popover: {
        pointerEvents: 'none',
    },
    paper: {
        padding: theme.spacing(1),
    },
}));

export default function MouseOverPopover() {
    const classes = useStyles();

    return (
        <div>
            <Popover
            style={{ position: 'absolute' }}
                disableScrollLock
                id="mouse-over-popover"
                className={classes.popover}
                classes={{
                    paper: classes.paper,
                }}
                open={true}
                anchorEl={document.getElementById("popoverContainer")}
                anchorOrigin={{
                    vertical: 'bottom',
                    horizontal: 'left',
                }}
                transformOrigin={{
                    vertical: 'top',
                    horizontal: 'left',
                }}
                onClose={() => {}}
                disableRestoreFocus
            >
                <Typography>I use Popover.</Typography>
            </Popover>
        </div>
    );
}
