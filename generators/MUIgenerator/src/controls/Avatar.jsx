import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Avatar from '@material-ui/core/Avatar';
import AvatarGroup from '@material-ui/lab/AvatarGroup';
import { deepOrange, deepPurple, green, pink } from '@material-ui/core/colors';
import FolderIcon from '@material-ui/icons/Folder';
import PageviewIcon from '@material-ui/icons/Pageview';
import AssignmentIcon from '@material-ui/icons/Assignment';

const useStyles = makeStyles((theme) => ({
    root: {
        display: 'flex',
        '& > *': {
            margin: theme.spacing(1),
        },
    },
    orange: {
        color: theme.palette.getContrastText(deepOrange[500]),
        backgroundColor: deepOrange[500],
    },
    purple: {
        color: theme.palette.getContrastText(deepPurple[500]),
        backgroundColor: deepPurple[500],
    },
    pink: {
        color: theme.palette.getContrastText(pink[500]),
        backgroundColor: pink[500],
    },
    green: {
        color: '#fff',
        backgroundColor: green[500],
    },
}));

export const JDIAvatar = ({ group, variant }) => {
    const classes = useStyles();

    const renderAvatar = ({ type }) => {
        const basic = [
            <Avatar key={type} data-label="avatar" variant={variant}>H</Avatar>,
            <Avatar key={type} data-label="avatar" variant={variant} className={classes.orange}>N</Avatar>,
            <Avatar key={type} data-label="avatar" variant={variant} className={classes.purple}>OP</Avatar>,
            <Avatar key={type} data-label="avatar" variant={variant} >
                <FolderIcon data-label="icon" />
            </Avatar>,
            <Avatar key={type} data-label="avatar" variant={variant} className={classes.pink}>
                <PageviewIcon data-label="icon" />
            </Avatar>,
            <Avatar key={type} data-label="avatar" variant={variant} className={classes.green}>
                <AssignmentIcon data-label="icon" />
            </Avatar>
        ];
        return basic[type];
    };

    const renderGroup = () => {
        if (group.length > 1) {
            return (<AvatarGroup>
                {
                    group.map(renderAvatar)
                }
            </AvatarGroup>)
        }
        return renderAvatar(group[0]);
    }

    return (
        <div>
            {renderGroup()}
        </div>
    );
}