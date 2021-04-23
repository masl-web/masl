import React, { useState, useEffect } from 'react';
import { Redirect, useHistory } from 'react-router';
import { Switch, Route, Link, BrowserRouter as Router } from "react-router-dom";
import axios from 'axios';
import { Container, Row, Col, Card } from 'react-bootstrap';
import Navbar from 'react-bootstrap/Navbar';
import './App.css';
import { Paper, makeStyles, Grid } from '@material-ui/core';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import Masl from './Masl';
import { textAlign } from '@material-ui/system';
import AreaDetail from './AreaDetail';
import UserInfo from './UserInfo';

import ModifiedUserInfo from './ModifiedUserInfo';

export default function App() {

  return (
    <Router>
      <Switch>
        <Route exact path='/' component={Index} />
        <Route path='/userinfo' component={UserInfo} />
        <Route path="/masl" component={Masl} />
        <Route path="/detail" component={AreaDetail} />

        <Route path="/temp" component={ModifiedUserInfo} /> 
        {/* hover 부분 변경한 UserInfo 페이지 /temp에 라우팅 by 이슬 */}
      </Switch>
    </Router>
  )
}


function Index() {

  const useStyles = makeStyles((theme) => ({
    root: {
      flexGrow: 1,
    },
    menuButton: {
      marginRight: theme.spacing(2),
    },
    title: {
      flexGrow: 1,
    },
    subtitle: {
      flexGrow: 2,
      color: 'white',
      textAlign: 'right'
    }
  }));
  const classes = useStyles();
  const history = useHistory
  return (
    <div>
      <div className={classes.root}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" className={classes.title}>
              Masl
            </Typography>
            <Typography className={classes.subtitle}>나를 위한 동네, 마이 슬세권</Typography>
          </Toolbar>
        </AppBar>
      </div>
          <Grid item xs={12} style={{ marginTop: '10rem'}}>
          <Row>
            <Col item xs={3}><div></div></Col>
            <Col item xs={6}>
          <Container>
            <Paper>
              <Button color="primary" size="large" onClick={(e)=>window.location.replace('/userinfo')}>마슬 찾아보기</Button>
            </Paper>
          </Container>
          </Col>
          <Col item xs={3}><div></div></Col>
          </Row>
          </Grid>
    </div>
  )
}


function Information() {
  return (
    <div>

    </div>
  )
}