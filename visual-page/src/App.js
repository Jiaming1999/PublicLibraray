import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
} from 'react-router-dom';
import { makeStyles } from '@material-ui/core/styles';
import Drawer from '@material-ui/core/Drawer';
import AppBar from '@material-ui/core/AppBar';
import CssBaseline from '@material-ui/core/CssBaseline';
import Toolbar from '@material-ui/core/Toolbar';
import List from '@material-ui/core/List';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import HomeIcon from '@material-ui/icons/Home';
import AccountBoxIcon from '@material-ui/icons/AccountBox';
import IndeterminateCheckBoxIcon from '@material-ui/icons/IndeterminateCheckBox';
import MenuBookIcon from '@material-ui/icons/MenuBook';
import DescriptionIcon from '@material-ui/icons/Description';
import AddIcon from '@material-ui/icons/Add';
import AddBoxIcon from '@material-ui/icons/AddBox';
import Get from './components/Get';
import Put from './components/Put';
import Post from './components/Post';
import Delete from './components/Delete';
import TopAuthors from './components/TopAuthors';
import TopBooks from "./components/TopBooks";
import ScrapePage from './components/ScrapePage';

const drawerWidth = 240;

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
  },
  drawerPaper: {
    width: drawerWidth,
  },
  drawerContainer: {
    overflow: 'auto',
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing(3),
  },
  link: {
    textDecoration: "none",
    color: "black",
    '&:hover': {
      color: "blue",
    }
  },
}));

export default function App() {
  const classes = useStyles();
  return (
    <Router>
      <div className={classes.root}>
        <CssBaseline />
        <AppBar position="fixed" className={classes.appBar}>
          <Toolbar>
            <Typography variant="h6" noWrap>
              Public Library
            </Typography>
          </Toolbar>
        </AppBar>
        <Drawer
          className={classes.drawer}
          variant="permanent"
          classes={{
            paper: classes.drawerPaper,
          }}
        >
          <Toolbar />
          {ListContent(classes)}
        </Drawer>
        <main className={classes.content}>
          <Toolbar />
          <Switch>
            <Route path="/scrape">
              <ScrapePage />
            </Route>
            <Route path="/delete">
              <Delete />
            </Route>
            <Route path="/post">
              <Post />
            </Route>
            <Route path="/put">
              <Put />
            </Route>
            <Route path="/top-book">
              <TopBooks />
            </Route>
            <Route path="/top-author">
              <TopAuthors />
            </Route>
            <Route path="/">
              <Get />
            </Route>
          </Switch>
        </main>
      </div>
    </Router>
  );
}


function ListContent(classes) {
  return <div className={classes.drawerContainer}>
    <List>
      <ListItem>
        <ListItemIcon>
          <HomeIcon />
        </ListItemIcon>
        <ListItemText>
          <Link className={classes.link} to="/">GetInfo</Link>
        </ListItemText>
      </ListItem>
      <ListItem>
        <ListItemIcon>
          <AddIcon />
        </ListItemIcon>
        <ListItemText>
          <Link className={classes.link} to="/put">UpdateInfo</Link>
        </ListItemText>
      </ListItem>
      <ListItem>
        <ListItemIcon>
          <AddBoxIcon />
        </ListItemIcon>
        <ListItemText>
          <Link className={classes.link} to="/post">PostContent</Link>
        </ListItemText>
      </ListItem>
      <ListItem>
        <ListItemIcon>
          <DescriptionIcon />
        </ListItemIcon>
        <ListItemText>
          <Link className={classes.link} to="/scrape">Scrape</Link>
        </ListItemText>
      </ListItem>
      <ListItem>
        <ListItemIcon>
          <IndeterminateCheckBoxIcon />
        </ListItemIcon>
        <ListItemText>
          <Link className={classes.link} to="/delete">DeleteContent</Link>
        </ListItemText>
      </ListItem>
      <ListItem>
        <ListItemIcon>
          <MenuBookIcon />
        </ListItemIcon>
        <ListItemText>
          <Link className={classes.link} to="/top-book">TopBooks</Link>
        </ListItemText>
      </ListItem>
      <ListItem>
        <ListItemIcon>
          <AccountBoxIcon />
        </ListItemIcon>
        <ListItemText>
          <Link className={classes.link} to="/top-author">TopAuthors</Link>
        </ListItemText>
      </ListItem>
    </List>
    <Divider />
  </div>;
}

