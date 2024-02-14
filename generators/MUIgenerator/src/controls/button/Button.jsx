import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import ArrowDownwardIcon from '@material-ui/icons/ArrowDownward';
import DeleteIcon from '@material-ui/icons/Delete';
import CloudUploadIcon from '@material-ui/icons/CloudUpload';
import KeyboardVoiceIcon from '@material-ui/icons/KeyboardVoice';
import Icon from '@material-ui/core/Icon';
import SaveIcon from '@material-ui/icons/Save';
import JDIComplexButton from './ComplexButton';

const useStyles = makeStyles((theme) => ({
    margin: {
        margin: theme.spacing(1),
    },
    extendedIcon: {
        marginRight: theme.spacing(1),
    },
    button: {
        margin: theme.spacing(1),
    }
}));

export default function JDIButton({ type }) {
    const classes = useStyles();

    return (
        <React.Fragment>
            {(type === 0) &&
                <React.Fragment>
                    <Button data-label="button" size="small" className={classes.margin}>
                        Small
                    </Button>
                    <Button data-label="button" size="medium" className={classes.margin}>
                        Medium
                    </Button>
                    <Button data-label="button" size="large" className={classes.margin}>
                        Large
                    </Button>
                </React.Fragment>
            }
            {(type === 1) &&
                <React.Fragment>
                    <Button data-label="button" variant="outlined" size="small" color="primary" className={classes.margin}>
                        Small
                    </Button>
                    <Button data-label="button" variant="outlined" size="medium" color="primary" className={classes.margin}>
                        Medium
                    </Button>
                    <Button data-label="button" variant="outlined" size="large" color="primary" className={classes.margin}>
                        Large
                    </Button>
                </React.Fragment>
            }
            {(type === 2) &&
                <React.Fragment>
                    <Button data-label="button" variant="contained" size="small" color="primary" className={classes.margin}>
                        Small
                    </Button>
                    <Button data-label="button" variant="contained" size="medium" color="primary" className={classes.margin}>
                        Medium
                    </Button>
                    <Button data-label="button" variant="contained" size="large" color="primary" className={classes.margin}>
                        Large
                    </Button>
                </React.Fragment>
            }
            {(type === 3) &&
                <React.Fragment>
                    <IconButton data-label="button" aria-label="delete" className={classes.margin} size="small">
                        <ArrowDownwardIcon fontSize="inherit" />
                    </IconButton>
                    <IconButton data-label="button" aria-label="delete" className={classes.margin}>
                        <DeleteIcon fontSize="small" />
                    </IconButton>
                    <IconButton data-label="button" aria-label="delete" className={classes.margin}>
                        <DeleteIcon />
                    </IconButton>
                    <IconButton data-label="button" aria-label="delete" className={classes.margin}>
                        <DeleteIcon fontSize="large" />
                    </IconButton>
                </React.Fragment>
            }
            {(type === 4) &&
                <React.Fragment>
                    <Button data-label="button"
                        variant="contained"
                        color="secondary"
                        className={classes.button}
                        startIcon={<DeleteIcon />}
                    >
                        Delete
                    </Button>
                    {/* This Button uses a Font Icon, see the installation instructions in the Icon component docs. */}
                    <Button data-label="button"
                        variant="contained"
                        color="primary"
                        className={classes.button}
                        endIcon={<Icon>send</Icon>}
                    >
                        Send
                    </Button>
                    <Button data-label="button"
                        variant="contained"
                        color="default"
                        className={classes.button}
                        startIcon={<CloudUploadIcon />}
                    >
                        Upload
                    </Button>
                    <Button data-label="button"
                        variant="contained"
                        disabled
                        color="secondary"
                        className={classes.button}
                        startIcon={<KeyboardVoiceIcon />}
                    >
                        Talk
                    </Button>
                    <Button data-label="button"
                        variant="contained"
                        color="primary"
                        size="small"
                        className={classes.button}
                        startIcon={<SaveIcon />}
                    >
                        Save
                    </Button>
                    <Button data-label="button"
                        variant="contained"
                        color="primary"
                        size="large"
                        className={classes.button}
                        startIcon={<SaveIcon />}
                    >
                        Save
                    </Button>
                </React.Fragment>
            }
            {(type === 5) &&
                <React.Fragment>
                   <JDIComplexButton />
                </React.Fragment>
            }
        </React.Fragment>)
}