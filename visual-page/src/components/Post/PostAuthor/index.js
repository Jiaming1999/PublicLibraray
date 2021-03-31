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

const PostAuthor = (props) => {
  const classes = useStyles(props)
  const [id, setId] = useState("")
  const [book, setBook] = useState("")
  const [rating, setRating] = useState(0.0)
  const [rating_count, setRatingCount] = useState(0)
  const [review_count, setReviewCount] = useState(0)
  const [name, setName] = useState("")
  const [url, setUrl] = useState("")

  const handleSubmit = (e) => {
    e.preventDefault()
    let tempUrl = 'http://127.0.0.1:5000/author'
    let authorBooks = book.split("/")
    let tempData = {
      "_id": id,
      "author_id": id,
      "author_book": authorBooks,
      "author_rating": parseFloat(rating),
      "author_rating_counts": parseInt(rating_count),
      "author_review_counts": parseInt(review_count),
      "author_name": name,
      "author_url": url
    }
    props.setData(tempData)
    props.setUrl(tempUrl)
  }



  return (
    <div className={classes.root}>
      <form className={classes.root} autoComplete="off" onSubmit={handleSubmit}>
        <TextField className={classes.text} id="standard-id" label="AuthorId" value={id} onChange={(e) => setId(e.target.value)} />
        <TextField className={classes.text} id="standard-author" label="AuthorBook" value={book} onChange={(e) => setBook(e.target.value)} />
        <TextField className={classes.text} id="standard-rating" label="AuthorRating" value={rating} onChange={(e) => setRating(e.target.value < 0 ? 0 : e.target.value)} />
        <TextField className={classes.text} id="standard-rc" label="AuthorRatingCount" value={rating_count} onChange={(e) => setRatingCount(e.target.value < 0 ? 0 : e.target.value)} />
        <TextField className={classes.text} id="standard-rec" label="AuthorReviewCount" value={review_count} onChange={(e) => setReviewCount(e.target.value < 0 ? 0 : e.target.value)} />
        <TextField className={classes.text} id="standard-title" label="AuthorName" value={name} onChange={(e) => setName(e.target.value)} />
        <TextField className={classes.text} id="standard-url" label="AuthorURL" value={url} onChange={(e) => setUrl(e.target.value)} />
        <button className={classes.button} type='submit'>
          Submit
        </button>
      </form>
    </div>
  )
}

export default PostAuthor