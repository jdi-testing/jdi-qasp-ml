import React from 'react';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';

export default function JDISwitch({ type }) {
    const [state, setState] = React.useState({
        checkedA: true,
        checkedB: true,
    });

    const handleChange = (event) => {
        setState({ ...state, [event.target.name]: event.target.checked });
    };

    return (
        <FormGroup row>
            {(type === 0) && <FormControlLabel
                control={<Switch checked={state.checkedA} onChange={handleChange} name="checkedA" />}
                label="Secondary"
            />}
            {(type === 1) && 
            <FormControlLabel
                control={
                    <Switch
                        checked={state.checkedB}
                        onChange={handleChange}
                        name="checkedB"
                        color="primary"
                    />
                }
                label="Primary"
            />}
            {(type === 2) && <FormControlLabel control={<Switch />} label="Uncontrolled" />}
            {(type === 3) && <FormControlLabel disabled control={<Switch />} label="Disabled" />}
            {(type === 4) && <FormControlLabel disabled control={<Switch checked />} label="Disabled" />}
        </FormGroup>
    );
}
