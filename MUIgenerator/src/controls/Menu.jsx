import React from 'react';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';

export default function JDIMenu() {
    const handleClose = () => {
    };

    return (
        <div id="menuDiv">
            <Menu
                id="simple-menu"
                keepMounted
                disableScrollLock
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
