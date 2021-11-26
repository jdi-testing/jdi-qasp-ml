import React from 'react';
import clsx from 'clsx';
import { makeStyles, useTheme } from '@material-ui/core/styles';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import ListItemText from '@material-ui/core/ListItemText';
import Select from '@material-ui/core/Select';
import Checkbox from '@material-ui/core/Checkbox';
import Chip from '@material-ui/core/Chip';

const useStyles = makeStyles((theme) => ({
    formControl: {
        margin: theme.spacing(1),
        minWidth: 120,
        maxWidth: 300,
    },
    chips: {
        display: 'flex',
        flexWrap: 'wrap',
    },
    chip: {
        margin: 2,
    },
    noLabel: {
        marginTop: theme.spacing(3),
    },
}));

const names = [
    'Oliver Hansen',
    'Van Henry',
    'April Tucker',
    'Ralph Hubbard',
    'Omar Alexander',
    'Carlos Abbott',
    'Miriam Wagner',
    'Bradley Wilkerson',
    'Virginia Andrews',
    'Kelly Snyder',
];

function getStyles(name, personName, theme) {
    return {
        fontWeight:
            personName.indexOf(name) === -1
                ? theme.typography.fontWeightRegular
                : theme.typography.fontWeightMedium,
    };
}

export default function JDIMultipleSelect({ type, open }) {
    const classes = useStyles();
    const theme = useTheme();
    const [personName, setPersonName] = React.useState([]);

    const handleChange = (event) => {
        setPersonName(event.target.value);
    };

    const handleChangeMultiple = (event) => {
        const { options } = event.target;
        const value = [];
        for (let i = 0, l = options.length; i < l; i += 1) {
            if (options[i].selected) {
                value.push(options[i].value);
            }
        }
        setPersonName(value);
    };

    return (
        <div>
            {(type === 0) && <FormControl className={classes.formControl}>
                <InputLabel id="demo-mutiple-name-label">Name</InputLabel>
                <Select data-label="select"  open={open}
                    MenuProps={{
                        disableScrollLock: true,
                    }}
                    labelId="demo-mutiple-name-label"
                    id="demo-mutiple-name"
                    multiple
                    value={personName}
                    onChange={handleChange}
                    input={<Input />}
                >
                    {names.map((name) => (
                        <MenuItem key={name} value={name} style={getStyles(name, personName, theme)}>
                            {name}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
            }
            {(type === 1) && <FormControl className={classes.formControl}>
                <InputLabel id="demo-mutiple-checkbox-label">Tag</InputLabel>
                <Select data-label="select"  open={open}
                    MenuProps={{
                        disableScrollLock: true,
                    }}
                    labelId="demo-mutiple-checkbox-label"
                    id="demo-mutiple-checkbox"
                    multiple
                    value={personName}
                    onChange={handleChange}
                    input={<Input />}
                    renderValue={(selected) => selected.join(', ')}
                >
                    {names.map((name) => (
                        <MenuItem key={name} value={name}>
                            <Checkbox data-label="checkbox"  checked={personName.indexOf(name) > -1} />
                            <ListItemText primary={name} />
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
            }
            {(type === 2) && <FormControl className={classes.formControl}>
                <InputLabel id="demo-mutiple-chip-label">Chip</InputLabel>
                <Select data-label="select"  open={open}
                    MenuProps={{
                        disableScrollLock: true,
                    }}
                    labelId="demo-mutiple-chip-label"
                    id="demo-mutiple-chip"
                    multiple
                    value={personName}
                    onChange={handleChange}
                    input={<Input id="select-multiple-chip" />}
                    renderValue={(selected) => (
                        <div className={classes.chips}>
                            {selected.map((value) => (
                                <Chip data-label="chip" key={value} label={value} className={classes.chip} />
                            ))}
                        </div>
                    )}
                >
                    {names.map((name) => (
                        <MenuItem key={name} value={name} style={getStyles(name, personName, theme)}>
                            {name}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
            }
            {(type === 3) && <FormControl className={clsx(classes.formControl, classes.noLabel)}>
                <Select data-label="select"  open={open}
                    MenuProps={{
                        disableScrollLock: true,
                    }}
                    // container={() => document.getElementById('selectDiv2')}
                    multiple
                    displayEmpty
                    value={personName}
                    onChange={handleChange}
                    input={<Input />}
                    renderValue={(selected) => {
                        if (selected.length === 0) {
                            return <em>Placeholder</em>;
                        }

                        return selected.join(', ');
                    }}
                    inputProps={{ 'aria-label': 'Without label' }}
                >
                    <MenuItem disabled value="">
                        <em>Placeholder</em>
                    </MenuItem>
                    {names.map((name) => (
                        <MenuItem key={name} value={name} style={getStyles(name, personName, theme)}>
                            {name}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
            }
            {(type === 4) && <FormControl className={classes.formControl}>
                <InputLabel shrink htmlFor="select-multiple-native">
                    Native
                </InputLabel>
                <Select data-label="select"  open={open}
                    MenuProps={{
                        disableScrollLock: true,
                    }}
                    multiple
                    native
                    value={personName}
                    onChange={handleChangeMultiple}
                    inputProps={{
                        id: 'select-multiple-native',
                    }}
                >
                    {names.map((name) => (
                        <option key={name} value={name}>
                            {name}
                        </option>
                    ))}
                </Select>
            </FormControl>
            }
        </div>
    );
}
