import React, { useState, useEffect } from "react"
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import BarChart from '../Barchart'
import { Card } from '@material-ui/core';

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
    margin: "5px",
    background: "##e7e7e7",
    border: "none",
    color: "black",
    padding: "15px 32px",
    textAlign: "center",
    text_decoration: "none",
    display: "inline-block",
  },
  bar: {
    fill: "black",
    height: "21px",
    transition: "fill .3s ease",
    cursor: "pointer",
    fontFamily: "Helvetica, sans-serif",
  },
  visual: {
  }
})

const TopBooks = (props) => {
  const classes = useStyles(props)
  const url = "http://127.0.0.1:5000/books"
  const [kth, setKth] = useState(1)
  const [data, setData] = useState([])
  const [tdata, setTData] = useState([]);
  const [msg, setMsg] = useState("")

  const changeData = () => {
    let temp_tdata = []
    for (let j = 0; j < data.length; j++) {
      temp_tdata.push(data[j][1] * 15)
    }
    setTData(temp_tdata);
  }

  /**
   * @https://stackoverflow.com/questions/1069666/sorting-object-property-by-values
   * how to sort obj property
   */
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
    }).then(data => {
      let sortableData = []
      for (let book in data) {
        sortableData.push([book, data[book]])
      }
      sortableData.sort(function (a, b) {
        return b[1] - a[1]
      })
      setData(sortableData)
    })
      .catch(err => {
        console.log(err)
      })
  }, [kth])

  const Visual = () => (
    <div className={classes.visual}>
      <h4>Top Books</h4>
      <Card className={classes.content}>
        {data.map(([title, rating], index) => (
          <p key={index}>{index + 1}:{title}:{rating}</p>
        ))}
      </Card>
    </div>
  )

  const handleChange = (e) => {
    setKth(e.target.value)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    let tempData = []
    if (kth <= 0) {
      setKth(1)
    }
    if (kth > data.length) {
      setMsg("K is greater than size of books")
    } else {
      setMsg("")
    }
    for (let i = 0; i < data.length; i++) {
      tempData.push(data[i])
      if (i === kth - 1) {
        break;
      }
    }
    setData(tempData)
  }

  const InputK = () => (
    <form className={classes.root} noValidate autoComplete="off" onSubmit={handleSubmit}>
      <TextField
        id="standard-basic"
        label="TopKthBooks"
        value={kth}
        onChange={handleChange}
        helperText={msg} />
      <button className={classes.button} type='submit'>
        Submit
      </button>
    </form>
  )

  return (
    <div className={classes.root}>
      <InputK />
      <Visual />
      <button className={classes.button} onClick={changeData}>
        Load Graph
      </button>
      <BarChart width={800} height={400} data={tdata} />
    </div>
  )
}

export default TopBooks;