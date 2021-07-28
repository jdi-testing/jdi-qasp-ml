import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Breadcrumbs from '@material-ui/core/Breadcrumbs';
import Typography from '@material-ui/core/Typography';
import Link from '@material-ui/core/Link';
import NavigateNextIcon from '@material-ui/icons/NavigateNext';
import HomeIcon from '@material-ui/icons/Home';
import WhatshotIcon from '@material-ui/icons/Whatshot';
import GrainIcon from '@material-ui/icons/Grain';

const useStyles = makeStyles((theme) => ({
    root: {
        '& > * + *': {
            marginTop: theme.spacing(2),
        },
    },
}));

function handleClick(event) {
    event.preventDefault();
    console.info('You clicked a breadcrumb.');
}

export default function JDIBreadcrumbs({type}) {
    const classes = useStyles();

    return (
        <React.Fragment>
            {(type === 0) && <div className={classes.root}>
                <Breadcrumbs separator="›" aria-label="breadcrumb">
                    <Link color="inherit" href="/" onClick={handleClick}>
                        Material-UI
                    </Link>
                    <Link color="inherit" href="/getting-started/installation/" onClick={handleClick}>
                        Core
                    </Link>
                    <Typography color="textPrimary">Breadcrumb</Typography>
                </Breadcrumbs>
                <Breadcrumbs separator="-" aria-label="breadcrumb">
                    <Link color="inherit" href="/" onClick={handleClick}>
                        Material-UI
                    </Link>
                    <Link color="inherit" href="/getting-started/installation/" onClick={handleClick}>
                        Core
                    </Link>
                    <Typography color="textPrimary">Breadcrumb</Typography>
                </Breadcrumbs>
                <Breadcrumbs separator={<NavigateNextIcon data-label="icon" fontSize="small" />} aria-label="breadcrumb">
                    <Link color="inherit" href="/" onClick={handleClick}>
                        Material-UI
                    </Link>
                    <Link color="inherit" href="/getting-started/installation/" onClick={handleClick}>
                        Core
                    </Link>
                    <Typography color="textPrimary">Breadcrumb</Typography>
                </Breadcrumbs>
            </div>}
            {(type === 1) &&
                <Breadcrumbs aria-label="breadcrumb">
                    <Link color="inherit" href="/" onClick={handleClick}>
                        Material-UI
                    </Link>
                    <Link color="inherit" href="/getting-started/installation/" onClick={handleClick}>
                        Core
                    </Link>
                    <Link
                        color="textPrimary"
                        href="/components/breadcrumbs/"
                        onClick={handleClick}
                        aria-current="page"
                    >
                        Breadcrumb
                    </Link>
                </Breadcrumbs>
            }
            {(type === 2) &&
                <Breadcrumbs aria-label="breadcrumb">
                    <Link color="inherit" href="/" onClick={handleClick} className={classes.link}>
                        <HomeIcon data-label="icon" className={classes.icon} />
                        Material-UI
                    </Link>
                    <Link
                        color="inherit"
                        href="/getting-started/installation/"
                        onClick={handleClick}
                        className={classes.link}
                    >
                        <WhatshotIcon data-label="icon" className={classes.icon} />
                        Core
                    </Link>
                    <Typography color="textPrimary" className={classes.link}>
                        <GrainIcon data-label="icon" className={classes.icon} />
                        Breadcrumb
                    </Typography>
                </Breadcrumbs>
            }
        </React.Fragment>
    );
}
