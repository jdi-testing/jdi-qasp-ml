import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import clsx from 'clsx';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import Typography from '@material-ui/core/Typography';
import { red } from '@material-ui/core/colors';
import FavoriteIcon from '@material-ui/icons/Favorite';
import ShareIcon from '@material-ui/icons/Share';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

const useStyles = makeStyles((theme) => ({
    root: {
        maxWidth: 345,
    },
    media: {
        height: 0,
        paddingTop: '56.25%', // 16:9
    },
    expand: {
        transform: 'rotate(0deg)',
        marginLeft: 'auto',
        transition: theme.transitions.create('transform', {
            duration: theme.transitions.duration.shortest,
        }),
    },
    expandOpen: {
        transform: 'rotate(180deg)',
    },
    avatar: {
        backgroundColor: red[500],
    },
}));

export default function JDICard({ variant, header, content, actionText, action }) {
    const classes = useStyles();
    const [expanded, setExpanded] = React.useState(false);

    const handleExpandClick = () => {
        setExpanded(!expanded);
    };

    const actions = [
        <IconButton data-label="button" aria-label="add to favorites">
            <FavoriteIcon data-label="icon" />
        </IconButton>,
        <IconButton data-label="button" aria-label="share">
            <ShareIcon  data-label="icon"/>
        </IconButton>,
        <IconButton
            className={clsx(classes.expand, {
                [classes.expandOpen]: expanded,
            })}
            onClick={handleExpandClick}
            aria-expanded={expanded}
            aria-label={action}
        >
            <ExpandMoreIcon data-label="icon" />
        </IconButton>,
        <Button data-label="button"  size="small">{actionText}</Button>
    ]

    return (
        <Card className={classes.root} data-label="card" {...{ variant }}>
            <CardHeader
                title={header}
                subheader={header}
            />
            <CardContent>
                <Typography data-label="typography" variant="body2" color="textSecondary" component="p">
                    {content}
                </Typography>
            </CardContent>
            <CardActions disableSpacing>
                {actions[action]}
            </CardActions>
        </Card>
    );
}
