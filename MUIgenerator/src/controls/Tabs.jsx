import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import PhoneIcon from '@material-ui/icons/Phone';
import FavoriteIcon from '@material-ui/icons/Favorite';
import PersonPinIcon from '@material-ui/icons/PersonPin';
import HelpIcon from '@material-ui/icons/Help';
import ShoppingBasket from '@material-ui/icons/ShoppingBasket';
import ThumbDown from '@material-ui/icons/ThumbDown';
import ThumbUp from '@material-ui/icons/ThumbUp';

const useStyles = makeStyles({
    root: {
        flexGrow: 1,
        maxWidth: 500,
    },
});

export default function JDITabs({ tabs, icons, ...rest }) {
    const classes = useStyles();    

    const renderIconsTab = (item, index) => {
        const iconTabs = [
            <Tab key={`${item.label}${index}`} icon={<PhoneIcon data-label="icon" />} />,
            <Tab key={`${item.label}${index}`} icon={<FavoriteIcon data-label="icon" />} />,
            <Tab key={`${item.label}${index}`} icon={<PersonPinIcon data-label="icon" />} />,
            <Tab key={`${item.label}${index}`} icon={<HelpIcon data-label="icon" />} />,
            <Tab key={`${item.label}${index}`} icon={<ShoppingBasket data-label="icon" />} />,
            <Tab key={`${item.label}${index}`} icon={<ThumbDown data-label="icon" />} />,
            <Tab key={`${item.label}${index}`} icon={<ThumbUp data-label="icon" />} />,
        ]
        return iconTabs[item];
    }

    const renderBasicTab = (item, index) => {
        return <Tab {...item} key={`${item.label}${index}`} />
    };

    return (
        <Paper data-label="paper"  square className={classes.root}>
            <Tabs data-label="tabs"
                onChange={() => {}}                                
                indicatorColor="primary"
                textColor="primary"
                aria-label="icon tabs example"
                {...rest}
            >
                {
                    tabs.map(icons ? renderIconsTab : renderBasicTab)
                }
            </Tabs>
        </Paper>
    );
}
