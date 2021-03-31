import React, { useState, useEffect } from "react"
import { makeStyles } from '@material-ui/core/styles';
import GetBook from './GetBook'
import GetAuthor from './GetAuthor'

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

const Get = (props) => {
  const classes = useStyles(props)
  const [url, setUrl] = useState("")
  const [data, setData] = useState()

  useEffect(() => {
    fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    }).then(response => {
      if (response.ok) {
        return response.json()
      }
    }).then(data => setData(data))
      .catch(err => {
        console.log(err)
        setData()
      })
  }, [url])

  const PrintOut = () => {
    if (data) {
      let temp_data = data
      return Object.keys(temp_data).map((key) => (
        <div key={key}>{key} =&gt; {temp_data[key]}</div>
      ))
    } else {
      return (<div>
        No data currently, Please reinput the field and check value validation
      </div>)
    }
  }

  return (
    <div className={classes.root}>
      <GetBook setUrl={setUrl} />
      <GetAuthor setUrl={setUrl} />
      <div className={classes.content}>
        <PrintOut />
      </div>
    </div>)
}

export default Get;