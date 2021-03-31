import React, { useState } from 'react'
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';

const useStyles = makeStyles({
  root: {
    padding: "5px",
    margin: "5px"
  },
  content: {
    padding: "5px",
    margin: "5px"
  },
  button: {
    background: "##e7e7e7",
    border: "none",
    color: "black",
    padding: "15px 32px",
    textAlign: "center",
    text_decoration: "none",
    display: "inline-block",
    margin: "10px"
  },
  text: {
    margin: "10px",
  }
})

const Scrape = (props) => {
  const classes = useStyles(props)
  const [value, setValue] = useState("")

  const handleSubmit = (e) => {
    e.preventDefault()
    let tempUrl = "http://127.0.0.1:5000/scrape?attr=" + value
    props.setUrl(tempUrl)
    setValue("")
  }

  return (
    <div className={classes.root}>
      <form className={classes.root} noValidate autoComplete="off" onSubmit={handleSubmit}>
        <TextField className={classes.text} id="standard-id" label="ScrapeURL" fullWidth={true} value={value} onChange={(e) => setValue(e.target.value)} />
        <button className={classes.button} type='submit'>
          Submit
        </button>
      </form>
    </div>
  )
}

export default Scrape