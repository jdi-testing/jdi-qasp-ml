import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Chip from '@material-ui/core/Chip';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import Divider from '@material-ui/core/Divider';
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
    maxWidth: 360,
    backgroundColor: theme.palette.background.paper,
  },
  chip: {
    margin: theme.spacing(0.5),
  },
  section1: {
    margin: theme.spacing(3, 2),
  },
  section2: {
    margin: theme.spacing(2),
  },
  section3: {
    margin: theme.spacing(3, 1, 1),
  },
}));

export default function MiddleDividers() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <div className={classes.section1}>
        <Grid data-label="grid" container alignItems="center">
          <Grid data-label="grid" item xs>
            <Typography data-label="typography" gutterBottom variant="h4">
              Toothbrush
            </Typography>
          </Grid>
          <Grid data-label="grid" item>
            <Typography data-label="typography" gutterBottom variant="h6">
              $4.50
            </Typography>
          </Grid>
        </Grid>
        <Typography data-label="typography" color="textSecondary" variant="body2">
          Pinstriped cornflower blue cotton blouse takes you on a walk to the park or just down the
          hall.
        </Typography>
      </div>
      <Divider variant="middle" />
      <div className={classes.section2}>
        <Typography data-label="typography" gutterBottom variant="body1">
          Select type
        </Typography>
        <div>
          <Chip data-label="chip" className={classes.chip} label="Extra Soft" />
          <Chip data-label="chip" className={classes.chip} color="primary" label="Soft" />
          <Chip data-label="chip" className={classes.chip} label="Medium" />
          <Chip data-label="chip" className={classes.chip} label="Hard" />
        </div>
      </div>
      <div className={classes.section3}>
        <Button data-label="button"  color="primary">Add to cart</Button>
      </div>
    </div>
  );
}
