import * as React from 'react';
import TextField from '@mui/material/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';

export default function JDIAutocomplete() {
  return (
    <Autocomplete
      data-label="select"
      disablePortal
      options={top100Films}
      sx={{ width: 300 }}
      renderInput={(params) => <TextField {...params} label="Movie" />}
      labelId="demo-autocomplete-helper-label"
      id="demo-autocomplete-helper"
    />
  );
}

const top100Films = [
  { label: 'The Shawshank Redemption', year: 1994 },
  { label: 'The Godfather', year: 1972 },
  { label: 'The Godfather: Part II', year: 1974 },
  { label: 'The Dark Knight', year: 2008 },
]