import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import MenuItem from '@material-ui/core/MenuItem';

const attribute = [
  {
    value: 'id',
    label: 'id',
  },
  {
    value: 'name',
    label: 'name',
  },
];

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
      width: '25ch',
    },
  },
  button: {
    margin: "10px",
    background: "##e7e7e7",
    border: "none",
    color: "black",
    padding: "15px 32px",
    textAlign: "center",
    text_decoration: "none",
    display: "inline-block",
  },
}));

const GetAuthor = (props) => {
  const classes = useStyles();

  const [value, setValue] = useState("")
  const [attr, setAttr] = useState('id')

  const handleChange = (e) => {
    setValue(e.target.value)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    let tempUrl = "http://127.0.0.1:5000/author?" + attr + "=" + value
    console.log(tempUrl)
    props.setUrl(tempUrl)
    setValue("")
  }

  const handleSelect = (e) => {
    setAttr(e.target.value)
  }


  return (
    <>
      <form className={classes.root} noValidate autoComplete="off" onSubmit={handleSubmit}>
        <TextField
          id="standard-select-attribute"
          select
          label="Select"
          value={attr}
          onChange={handleSelect}
          helperText="Please select search key"
        >
          {attribute.map((option) => (
            <MenuItem key={option.value} value={option.value}>
              {option.label}
            </MenuItem>
          ))}
        </TextField>
        <TextField id="standard-basic" label="AuthorId" value={value} onChange={handleChange} />
        <button className={classes.button}>
          Submit
        </button>
      </form>
    </>
  )
}

export default GetAuthor