import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Divider from '@material-ui/core/Divider';

const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
    maxWidth: 360,
    backgroundColor: theme.palette.background.paper,
  },
}));

export default function ListDividers() {
  const classes = useStyles();

  return (
    <List data-label="list" component="nav" className={classes.root} aria-label="mailbox folders">
      <ListItem button data-label="button">
        <ListItemText primary="Inbox22" />
      </ListItem>
      <Divider data-label="divider"/>
      <ListItem button divider data-label="button">
        <ListItemText primary="Drafts" />
      </ListItem>
      <ListItem button data-label="button">
        <ListItemText primary="Trash" />
      </ListItem>
      <Divider data-label="divider" light />
      <ListItem button data-label="button">
        <ListItemText primary="Spam" />
      </ListItem>
    </List>
  );
}
