import React, { useState, useEffect } from 'react';
import { Redirect, useHistory } from 'react-router';
import { Switch, Route, Link, BrowserRouter as Router } from "react-router-dom";
import axios from 'axios';
import Home from './routes/Home';
import { Container, Row, Col, Card } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import Navbar from 'react-bootstrap/Navbar';
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
        <Route exact path='/' component={Home} />
        <Route path='/userinfo' component={UserInfo} />
        <Route path="/masl" component={Masl} />
        <Route path="/detail" component={AreaDetail} />

        <Route path="/temp" component={ModifiedUserInfo} /> 
        {/* hover 부분 변경한 UserInfo 페이지 /temp에 라우팅 by 이슬 */}
      </Switch>
    </Router>
  )
}
