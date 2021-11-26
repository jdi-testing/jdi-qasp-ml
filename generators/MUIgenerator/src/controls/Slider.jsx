import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Slider from '@material-ui/core/Slider';

const useStyles = makeStyles({
    root: {
        width: 200,
        margin: '10px',
        height: 300,
    },
});

export default function ContinuousSlider(props) {
    const classes = useStyles();

    return (
        <div className={classes.root}>
            <Slider data-label="slider" onChange={() => {}}  {...props} />
        </div>
    );
}
