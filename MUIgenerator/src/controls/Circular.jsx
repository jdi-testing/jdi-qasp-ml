import React from 'react';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/core/styles';
import CircularProgress from '@material-ui/core/CircularProgress';
import { green } from '@material-ui/core/colors';
import Button from '@material-ui/core/Button';
import Fab from '@material-ui/core/Fab';
import CheckIcon from '@material-ui/icons/Check';
import SaveIcon from '@material-ui/icons/Save';
import { LinearProgress } from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
    root1: {
        width: '100%',
        '& > * + *': {
            marginTop: theme.spacing(2),
        },
    },
    root: {
        display: 'flex',
        alignItems: 'center',
    },
    wrapper: {
        margin: theme.spacing(1),
        position: 'relative',
    },
    buttonSuccess: {
        backgroundColor: green[500],
        '&:hover': {
            backgroundColor: green[700],
        },
    },
    fabProgress: {
        color: green[500],
        position: 'absolute',
        top: -6,
        left: -6,
        zIndex: 1,
    },
    buttonProgress: {
        color: green[500],
        position: 'absolute',
        top: '50%',
        left: '50%',
        marginTop: -12,
        marginLeft: -12,
    },
}));

export default function CircularIntegration({ type }) {
    const classes = useStyles();
    const [loading, setLoading] = React.useState(false);
    const [success, setSuccess] = React.useState(false);
    const timer = React.useRef();

    const buttonClassname = clsx({
        [classes.buttonSuccess]: success,
    });

    React.useEffect(() => {
        return () => {
            clearTimeout(timer.current);
        };
    }, []);

    const handleButtonClick = () => {
        if (!loading) {
            setSuccess(false);
            setLoading(true);
            timer.current = window.setTimeout(() => {
                setSuccess(true);
                setLoading(false);
            }, 2000);
        }
    };

    return (
        <React.Fragment>
            <div className={classes.root}>
                {(type === 0) && <CircularProgress data-label="progress"  variant="determinate" value={75} />}
                {(type === 1) && <CircularProgress data-label="progress"  color="secondary" />}
                {(type === 2) && <div className={classes.wrapper}>
                    <Fab
                        aria-label="save"
                        color="primary"
                        className={buttonClassname}
                        onClick={handleButtonClick}
                    >
                        {success ? <CheckIcon data-label="icon" /> : <SaveIcon data-label="icon" />}
                    </Fab>
                    <CircularProgress data-label="progress"  size={68} className={classes.fabProgress} />
                </div>}
                {(type === 3) && <div className={classes.wrapper}>
                    <Button data-label="button" 
                        variant="contained"
                        color="primary"
                        className={buttonClassname}
                        disabled={loading}
                        onClick={handleButtonClick}
                    >
                        Accept terms
                    </Button>
                    <CircularProgress data-label="progress"  size={24} className={classes.buttonProgress} />
                </div>}
            </div>
            <div className={classes.roo1}>
                {(type === 4) && <LinearProgress data-label="progress"  />}
                {(type === 5) && <LinearProgress data-label="progress"  color="secondary" />}
            </div>
        </React.Fragment>
    );
}
