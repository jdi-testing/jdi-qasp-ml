import React from 'react';
import Portal from '@material-ui/core/Portal';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  alert: {
    padding: theme.spacing(1),
    margin: theme.spacing(1, 0),
    border: '1px solid',
  },
}));

export default function JDIPortal() {
  const classes = useStyles();
  const container = React.useRef(null);

  return (
    <div>
      <div className={classes.alert}>
        It looks like I will render here.
        {true ? (
          <Portal data-label="portal"  container={container.current}>
            <span>But I actually render here!</span>
          </Portal>
        ) : null}
      </div>
      <div className={classes.alert} ref={container} />
    </div>
  );
}
