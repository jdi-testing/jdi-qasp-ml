import React from 'react';
import MuiAlert from '@material-ui/lab/Alert';
import { makeStyles } from '@material-ui/core/styles';

function Alert(props) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}

const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
    '& > * + *': {
      marginTop: theme.spacing(2),
    },
  },
}));

export default function JDIAlert({ type, text }) {
  const classes = useStyles();

  const renderAlert = () => {
    return [
      <Alert data-label="alert" severity="error">{text}</Alert>,
      <Alert data-label="alert" severity="warning">{text}</Alert>,
      <Alert data-label="alert" severity="info">{text}</Alert>,
      <Alert data-label="alert" severity="success">{text}</Alert>
    ][type]
  }

  return (
    <div className={classes.root}>
      {renderAlert()}
    </div>
  );
}
