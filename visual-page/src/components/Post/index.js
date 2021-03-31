import React, { useState, useEffect } from 'react'
import { makeStyles } from '@material-ui/core/styles'
import { Card } from '@material-ui/core'
import PostBook from './PostBook'
import PostAuthor from './PostAuthor'

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

const Post = (props) => {
  const classes = useStyles(props)
  const [data, setData] = useState()
  const [url, setUrl] = useState("")
  const [msg, setMsg] = useState("Nothing to be posted")

  useEffect(() => {
    fetch(url, {
      method: 'POST',
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
        setMsg("Success Post!")
      }
    })
      .catch(err => {
        console.log(err, "Failed")
        setMsg("Failed to post, please check format and key of inputing value\n")
      })
  }, [url, data])

  const Hint = () => (
    <Card className={classes.hint}>
      In multi book authors situation, please follow format of author1/author2/... to insert authors<br />
      In multi author books situation, please follow same format as book authors, separate with "/"<br />
      All rating and counts should be positive, 0 otherwise input.
    </Card>
  )

  return (
    <div className={classes.root}>
      <PostBook setUrl={setUrl} setData={setData} />
      <PostAuthor setUrl={setUrl} setData={setData} />
      <div className={classes.content}>
        {msg}
      </div>
      <Hint />
    </div>

  )
}

export default Post