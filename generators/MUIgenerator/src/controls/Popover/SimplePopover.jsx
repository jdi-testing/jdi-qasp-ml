import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Popover from '@material-ui/core/Popover';
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles((theme) => ({
    typography: {
        padding: theme.spacing(2),
    },
}));

export default function SimplePopover() {
    const containerRef = React.useRef();
    const classes = useStyles();

    return (
        <div ref={containerRef}>
            <Popover data-label="popover" 
                style={{ position: 'absolute' }}
                disableScrollLock
                id="simple-popover"
                open
                onClose={() => { }}
                anchorOrigin={{
                    vertical: 'bottom',
                    horizontal: 'center',
                }}
                transformOrigin={{
                    vertical: 'top',
                    horizontal: 'center',
                }}
            >
                <Typography data-label="typography" className={classes.typography}>The content of the Popover.</Typography>
            </Popover>
        </div>
    );
}
