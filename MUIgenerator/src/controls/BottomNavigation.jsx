import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import BottomNavigation from '@material-ui/core/BottomNavigation';
import RestoreIcon from '@material-ui/icons/Restore';
import FavoriteIcon from '@material-ui/icons/Favorite';
import LocationOnIcon from '@material-ui/icons/LocationOn';
import FolderIcon from '@material-ui/icons/Folder';
import { BottomNavigationAction } from '@material-ui/core';

const useStyles = makeStyles({
    root: {
        width: 500,
    },
});

export default function JDIBottomNavigation({ type }) {
    const classes = useStyles();
    const [value, setValue] = React.useState(0);

    return (
        <React.Fragment>
            {(type === 0) && <BottomNavigation data-label="bottom-navigation" 
                value={value}
                onChange={(event, newValue) => {
                    setValue(newValue);
                }}
                showLabels
                className={classes.root}
            >
                <BottomNavigationAction label="Recents" icon={<RestoreIcon data-label="icon" />} />
                <BottomNavigationAction label="Favorites" icon={<FavoriteIcon data-label="icon" />} />
                <BottomNavigationAction label="Nearby" icon={<LocationOnIcon data-label="icon" />} />
            </BottomNavigation>}
            {(type === 1) && <BottomNavigation data-label="bottom-navigation"  value={value} onChange={() => {}} className={classes.root}>
                <BottomNavigationAction label="Recents" value="recents" icon={<RestoreIcon data-label="icon" />} />
                <BottomNavigationAction label="Favorites" value="favorites" icon={<FavoriteIcon data-label="icon" />} />
                <BottomNavigationAction label="Nearby" value="nearby" icon={<LocationOnIcon data-label="icon" />} />
                <BottomNavigationAction label="Folder" value="folder" icon={<FolderIcon data-label="icon" />} />
            </BottomNavigation>}
        </React.Fragment>

    );
}
