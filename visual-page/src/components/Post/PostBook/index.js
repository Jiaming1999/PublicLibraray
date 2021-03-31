import React, { useState } from "react"
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

const PostBook = (props) => {
  const classes = useStyles(props)
  const [id, setId] = useState("")
  const [author, setAuthor] = useState("")
  const [rating, setRating] = useState(0.0)
  const [rating_count, setRatingCount] = useState(0)
  const [review_count, setReviewCount] = useState(0)
  const [title, setTitle] = useState("")
  const [url, setUrl] = useState("")

  const handleSubmit = (e) => {
    e.preventDefault()
    let tempUrl = 'http://127.0.0.1:5000/book'
    let bookAuthors = author.split("/")
    let tempData = {
      "_id": id,
      "book_id": id,
      "book_author": bookAuthors,
      "book_rating": parseFloat(rating),
      "book_rating_count": parseInt(rating_count),
      "book_review_count": parseInt(review_count),
      "book_title": title,
      "book_url": url
    }
    props.setData(tempData)
    props.setUrl(tempUrl)
  }



  return (
    <div className={classes.root}>
      <form className={classes.root} noValidate autoComplete="off" onSubmit={handleSubmit}>
        <TextField className={classes.text} id="standard-id" label="BookId" value={id} onChange={(e) => setId(e.target.value)} />
        <TextField className={classes.text} id="standard-author" label="BookAuthor" value={author} onChange={(e) => setAuthor(e.target.value < 0 ? 0 : e.target.value)} />
        <TextField className={classes.text} id="standard-rating" label="BookRating" value={rating} onChange={(e) => setRating(e.target.value < 0 ? 0 : e.target.value)} />
        <TextField className={classes.text} id="standard-rc" label="BookRatingCount" value={rating_count} onChange={(e) => setRatingCount(e.target.value < 0 ? 0 : e.target.value)} />
        <TextField className={classes.text} id="standard-rec" label="BookReviewCount" value={review_count} onChange={(e) => setReviewCount(e.target.value < 0 ? 0 : e.target.value)} />
        <TextField className={classes.text} id="standard-title" label="BookTitle" value={title} onChange={(e) => setTitle(e.target.value)} />
        <TextField className={classes.text} id="standard-url" label="BookURL" value={url} onChange={(e) => setUrl(e.target.value)} />
        <button className={classes.button} type='submit'>
          Submit
        </button>
      </form>
    </div>
  )
}

export default PostBook