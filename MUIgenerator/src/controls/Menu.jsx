import React from 'react';
import Button from '@material-ui/core/Button';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';

export default function JDIMenu() {
    const handleClick = (event) => {
    };

    const handleClose = () => {
    };

    return (
        <div id="menuDiv">
            <Button data-label="button"  aria-controls="simple-menu" onClick={handleClick}>
                Open Menu
            </Button>
            <Menu
                id="simple-menu"
                keepMounted
                open
                onClose={handleClose}
                autoFocus={false}
                PaperProps={{
                    style: {
                        position: 'relative',
                        transform: 'translateX(80%) translateY(-10%)',
                    }
                }}
                MenuListProps={{
                    ["data-label"]: "menu",
                    style: {
                        padding: 0,
                    },
                }}

            >
                <MenuItem onClick={handleClose}>Profile</MenuItem>
                <MenuItem onClick={handleClose}>My account</MenuItem>
                <MenuItem onClick={handleClose}>Logout</MenuItem>
            </Menu>
        </div>
    );
}
