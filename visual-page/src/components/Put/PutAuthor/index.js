import React, { useState } from "react"
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import MenuItem from '@material-ui/core/MenuItem';

const keys = [
  {
    value: 'author_rating',
    label: 'rating',
  },
  {
    value: 'author_name',
    label: 'name',
  },
  {
    value: 'author_url',
    label: 'URL',
  },
  {
    value: 'author_review_counts',
    label: 'review count',
  },
  {
    value: 'author_rating_counts',
    label: 'rating count',
  },
];

const useStyles = makeStyles({
  root: {
    padding: "5px",
    margin: "5px"
  },
  text: {
    margin: "10px",
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
  }
}
)

const PutAuthor = (props) => {
  const classes = useStyles(props)
  const [id, setId] = useState("")
  const [value, setValue] = useState("")
  const [key, setKey] = useState("")

  const handleIdChange = (e) => {
    setId(e.target.value)
  }

  const handleChange = (e) => {
    setValue(e.target.value)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    let tempUrl = "http://127.0.0.1:5000/author?id=" + id
    props.setUrl(tempUrl)
    let tempJson = { [key]: value }
    props.setData(tempJson)
    setId("")
    setValue("")
  }

  const handleSelect = (e) => {
    setKey(e.target.value)
  }

  return (
    <>
      <form className={classes.root} noValidate autoComplete="off" onSubmit={handleSubmit}>
        <TextField className={classes.text} id="standard-id" label="AuthorId" value={id} onChange={handleIdChange} />
        <TextField
          className={classes.text}
          id="standard-select-attribute"
          select
          label="Select"
          value={key}
          onChange={handleSelect}
          helperText="Please select search key"
        >
          {keys.map((option) => (
            <MenuItem key={option.value} value={option.value}>
              {option.label}
            </MenuItem>
          ))}
        </TextField>
        <TextField className={classes.text} id="put-attr" label="UpdateAuthor" value={value} onChange={handleChange} />
        <button className={classes.button} type='submit'>
          Submit
        </button>
      </form>

    </>

  )
}

export default PutAuthor