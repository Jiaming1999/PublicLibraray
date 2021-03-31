import React, { useState, useEffect } from "react";
import { makeStyles } from '@material-ui/core/styles';
import DeleteAuthor from './DeleteAuthor';
import DeleteBook from './DeleteBook';

const useStyles = makeStyles({
  root: {
    padding: "5px",
    margin: "5px"
  },
  content: {
    padding: "5px",
    margin: "5px"
  }
})

const Delete = (props) => {
  const classes = useStyles(props)
  const [url, setUrl] = useState("")
  const [msg, setMsg] = useState("Nothing to be deleted, please start to input")

  useEffect(() => {
    fetch(url, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    }).then(response => {
      if (response.ok) {
        return response.json()
      }
    }).then(data => {
      console.log(data)
      if (data) {
        setMsg("Success Delete!")
      }
    })
      .catch(err => setMsg("Deleted failed, check your if id is valid", err))
  }, [url])

  return (
    <div className={classes.root}>
      <DeleteBook setUrl={setUrl} />
      <DeleteAuthor setUrl={setUrl} />
      <div className={classes.content}>
        {msg}
      </div>
    </div>)
}

export default Delete;