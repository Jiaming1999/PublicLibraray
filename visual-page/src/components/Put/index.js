import React, { useState, useEffect } from "react"
import { makeStyles } from '@material-ui/core/styles'
import PutBook from "./PutBook"
import PutAuthor from "./PutAuthor"
import { Card } from "@material-ui/core"


const useStyles = makeStyles({
  root: {
    padding: "5px",
    margin: "5px"
  },
  content: {
    padding: "5px",
    margin: "5px"
  },
  hint: {
    padding: "5px",
    margin: "5px"
  }
})

const Put = (props) => {
  const classes = useStyles(props)
  const [url, setUrl] = useState("http://127.0.0.1:5000/")
  const [data, setData] = useState({})
  const [msg, setMsg] = useState("Nothing has been put")

  useEffect(() => {
    fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    }).then(response => {
      if (response.ok) {
        return response.json()
      }
    }).then(data => {
      console.log(data)
      if (data) {
        setMsg("Success Put!")
      }
    })
      .catch(err => {
        console.log(err, "Failed")
        setMsg("Failed to put, please check format and key of inputing value\n"
          +
          "Or the field to update is not existing in the data structure")
      })
  }, [url, data])

  const Hint = () => (
    <Card className={classes.hint}>
      valid key update for book:<br />
      book_rating, isbn, book_title, book_url, book_review_count, book_rating_count. <br />
      valid key update for author:<br />
      author_name, author_rating, author_rating_counts, author_review_counts, author_url
    </Card>
  )


  return (
    <div className={classes.root}>
      <PutBook setUrl={setUrl} setData={setData} />
      <PutAuthor setUrl={setUrl} setData={setData} />
      <div className={classes.content}>
        {msg}
      </div>
      <Hint />
    </div>

  )
}

export default Put;