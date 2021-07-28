import React from 'react';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';

export default function JDIradio({ group, formLabel, labelPlacement, row }) {
    const [value, setValue] = React.useState('female');

    const handleChange = (event) => {
        setValue(event.target.value);
    };

    const renderSatndalone = () => {
        const { label, disabled } = group[0];
        return <Radio
            data-label="radio" 
            checked={value}
            onChange={handleChange}
            value={value}
            name={label}
            inputProps={{ 'aria-label': 'A' }}
            {...{ disabled }}
        />
    }

    const renderGroup = () => {
        return (
            <FormControl component="fieldset">
                <FormLabel component="legend">{formLabel}</FormLabel>
                <RadioGroup data-label="radiogroup"  aria-label="gender" name="gender1" value={value} onChange={handleChange} {...{ row }}>
                    {
                        group.map(({ label, disabled }, index) => {
                            return <FormControlLabel key={`${label}${index}`} value={label} control={<Radio data-label="radio" />} {...{ label, disabled, labelPlacement }} />
                        })
                    }
                </RadioGroup>
            </FormControl>
        )
    }

    return (
        <React.Fragment>
            {
                group.length > 1 ? renderGroup() : renderSatndalone()
            }
        </React.Fragment>

    );
}
