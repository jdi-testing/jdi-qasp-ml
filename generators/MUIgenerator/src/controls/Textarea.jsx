import React from 'react';
import TextareaAutosize from '@material-ui/core/TextareaAutosize';

export default function JDITextarea({type}) {
    return (
        <React.Fragment>
            {(type === 0) && <TextareaAutosize  data-label="textarea-autosize" 
                maxRows={4}
                aria-label="maximum height"
                placeholder="Maximum 4 rows"
                defaultValue="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt
          ut labore et dolore magna aliqua."
            />}
            {(type === 1) && <TextareaAutosize  data-label="textarea-autosize"  aria-label="minimum height" minRows={3} placeholder="Minimum 3 rows" />}
            {(type === 2) && <TextareaAutosize  data-label="textarea-autosize"  aria-label="empty textarea" placeholder="Empty" />}
        </React.Fragment>

    );
}
