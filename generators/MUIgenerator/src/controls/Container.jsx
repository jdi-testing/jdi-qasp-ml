import React from 'react';
import CssBaseline from '@material-ui/core/CssBaseline';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';

export const JDIContainer = ({ fixed, maxWidth, style, text }) => {
    return (
        <React.Fragment>
            <CssBaseline />
            <Container data-label="container"  fixed={fixed} maxWidth={maxWidth}>
                <Typography data-label="typography" component="div" style={style}>{text}</Typography>
            </Container>
        </React.Fragment>
    );
}