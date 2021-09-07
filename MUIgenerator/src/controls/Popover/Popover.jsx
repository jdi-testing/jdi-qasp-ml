import React from 'react';
import MouseOverPopover from './MouseOverPopover';
import SimplePopover from './SimplePopover';

export const JDIPopover = ({type}) => {
    return (
        <div id="popoverContainer">
            {(type === 0) && <SimplePopover />}
            {(type === 1) && <MouseOverPopover />}
        </div>
    )
}