import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import InputLabel from '@material-ui/core/InputLabel';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import NativeSelect from '@material-ui/core/NativeSelect';

const useStyles = makeStyles((theme) => ({
    formControl: {
        margin: theme.spacing(1),
        minWidth: 120,
    },
    selectEmpty: {
        marginTop: theme.spacing(2),
    },
}));

export default function JDINativeSelects({ type, open }) {
    const classes = useStyles();
    const [state, setState] = React.useState({
        age: '',
        name: 'hai',
    });

    const handleChange = (event) => {
        const name = event.target.name;
        setState({
            ...state,
            [name]: event.target.value,
        });
    };

    return (
        <div>
            {
                type === 0 && <FormControl className={classes.formControl}>
                    <InputLabel htmlFor="age-native-simple">Age</InputLabel>
                    <Select open={open}
                        MenuProps={{
                            disableScrollLock: true,
                        }}
                        native
                        value={state.age}
                        onChange={handleChange}
                        inputProps={{
                            name: 'age',
                            id: 'age-native-simple',
                        }}
                    >
                        <option aria-label="None" value="" />
                        <option value={10}>Ten</option>
                        <option value={20}>Twenty</option>
                        <option value={30}>Thirty</option>
                    </Select>
                </FormControl>
            }
            {type === 1 && <FormControl className={classes.formControl}>
                <InputLabel htmlFor="age-native-helper">Age</InputLabel>
                <NativeSelect open={open}
                    MenuProps={{
                        disableScrollLock: true,
                    }}
                    value={state.age}
                    onChange={handleChange}
                    inputProps={{
                        name: 'age',
                        id: 'age-native-helper',
                    }}
                >
                    <option aria-label="None" value="" />
                    <option value={10}>Ten</option>
                    <option value={20}>Twenty</option>
                    <option value={30}>Thirty</option>
                </NativeSelect>
                <FormHelperText>Some important helper text</FormHelperText>
            </FormControl>
            }
            {type === 2 && <FormControl className={classes.formControl}>
                <NativeSelect open={open}
                    MenuProps={{
                        disableScrollLock: true,
                    }}
                    value={state.age}
                    onChange={handleChange}
                    name="age"
                    className={classes.selectEmpty}
                    inputProps={{ 'aria-label': 'age' }}
                >
                    <option value="">None</option>
                    <option value={10}>Ten</option>
                    <option value={20}>Twenty</option>
                    <option value={30}>Thirty</option>
                </NativeSelect>
                <FormHelperText>With visually hidden label</FormHelperText>
            </FormControl>
            }
            {type === 3 && <FormControl className={classes.formControl}>
                <InputLabel shrink htmlFor="age-native-label-placeholder">
                    Age
                </InputLabel>
                <NativeSelect open={open}
                    MenuProps={{
                        disableScrollLock: true,
                    }}
                    value={state.age}
                    onChange={handleChange}
                    inputProps={{
                        name: 'age',
                        id: 'age-native-label-placeholder',
                    }}
                >
                    <option value="">None</option>
                    <option value={10}>Ten</option>
                    <option value={20}>Twenty</option>
                    <option value={30}>Thirty</option>
                </NativeSelect>
                <FormHelperText>Label + placeholder</FormHelperText>
            </FormControl>
            }
            {type === 4 &&
                <FormControl variant="filled" className={classes.formControl}>
                    <InputLabel htmlFor="filled-age-native-simple">Age</InputLabel>
                    <Select open={open}
                        MenuProps={{
                            disableScrollLock: true,
                        }}
                        native
                        value={state.age}
                        onChange={handleChange}
                        inputProps={{
                            name: 'age',
                            id: 'filled-age-native-simple',
                        }}
                    >
                        <option aria-label="None" value="" />
                        <option value={10}>Ten</option>
                        <option value={20}>Twenty</option>
                        <option value={30}>Thirty</option>
                    </Select>
                </FormControl>
            }
        </div>
    );
}
