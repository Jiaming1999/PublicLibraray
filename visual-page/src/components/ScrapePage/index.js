import React, { useState, useEffect } from 'react'
import { makeStyles } from '@material-ui/core/styles'
import { Card } from '@material-ui/core'
import Scrape from './Scrape'


const useStyles = makeStyles({
  root: {
    padding: "5px",
    margin: "5px"
  },
  content: {
    padding: "5px",
    margin: "5px",
  },
  hint: {
    padding: "10px",
    margin: "5px",
    marginTop: '10px'
  }
})

const ScrapePage = (props) => {
  const classes = useStyles(props)
  const [url, setUrl] = useState("")
  const [msg, setMsg] = useState("Nothing to be posted")

  useEffect(() => {
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    }).then(response => {
      if (response.ok) {
        setMsg("Success Post!")
        return
      }
    }).then(data => {
    })
      .catch(err => {
        console.log(err, "Failed")
        setMsg("Failed to post, please check format and key of inputing value\n")
      })
  }, [url])

  const Hint = () => (
    <Card className={classes.hint}>
      The correct format example usage:<br />
      book/show/xxx.BookName<br />
      author/show/xxx.AuthorName<br />
      You dont need goodreads prefix
    </Card>
  )

  return (
    <div className={classes.root}>
      <Scrape setUrl={setUrl} />
      <div className={classes.content}>
        {msg}
      </div>
      <Hint />
    </div>

  )
}

export default ScrapePage